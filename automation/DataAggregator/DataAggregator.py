from ..SocketInterface import serversocket
from ..MPLogger import loggingclient
from sqlite3 import OperationalError
from sqlite3 import ProgrammingError
from sqlite3 import IntegrityError 
import sqlite3
import time
import os


def DataAggregator(manager_params, status_queue, commit_batch_size=1000):
    """
     Receives SQL queries from other processes and writes them to the central database
     Executes queries until being told to die (then it will finish work and shut down)
     This process should never be terminated un-gracefully
     Currently uses SQLite but may move to different platform

     <manager_params> TaskManager configuration parameters
     <status_queue> is a queue connect to the TaskManager used for communication
     <commit_batch_size> is the number of execution statements that should be made before a commit (used for speedup)
    """

    # sets up DB connection
    db_path = manager_params['database_name']
    db = sqlite3.connect(db_path, check_same_thread=False)
    curr = db.cursor()

    # sets up logging connection
    logger = loggingclient(*manager_params['logger_address'])

    # sets up the serversocket to start accepting connections
    sock = serversocket()
    status_queue.put(sock.sock.getsockname())  # let TM know location
    sock.start_accepting()

    counter = 0  # number of executions made since last commit
    commit_time = 0  # keep track of time since last commit
    while True:
        # received KILL command from TaskManager
        if not status_queue.empty():
            status_queue.get()
            sock.close()
            drain_queue(sock.queue, curr, logger)
            break

        # no command for now -> sleep to avoid pegging CPU on blocking get
        if sock.queue.empty():
            time.sleep(0.001)

            # commit every five seconds to avoid blocking the db for too long
            if counter > 0 and time.time() - commit_time > 5:
                db.commit()
            continue

        # process query
        query = sock.queue.get()
        process_query(query, curr, logger)

        # batch commit if necessary
        counter += 1
        if counter >= commit_batch_size:
            counter = 0
            commit_time = time.time()
            db.commit()

    # finishes work and gracefully stops
    db.commit()
    db.close()


def process_query(query, curr, logger):
    """
    executes a query of form (template_string, arguments)
    query is of form (template_string, arguments)
    """
    
    if len(query) != 2:
        print "ERROR: Query is not the correct length"
        return
    statement = query[0]
    args = list(query[1])
    
    for i in range(len(args)):
        if type(args[i]) == str:
            args[i] = unicode(args[i], errors='ignore')
        elif callable(args[i]):
            args[i] = str(args[i])
    try:
        if len(args) == 0:
            curr.execute(statement)
        else:
            curr.execute(statement,args)
    except OperationalError as e:
        logger.error("Unsupported query 1" + '\n' + str(type(e)) + '\n' + str(e) + '\n' + statement + '\n' + str(args))
        pass
    except ProgrammingError as e:
        logger.error("Unsupported query 2" + '\n' + str(type(e)) + '\n' + str(e) + '\n' + statement + '\n' + str(args))
        pass
    except IntegrityError as e:
        print "1"
        logger.error("Integrity Error" + '\n' + str(type(e)) + '\n' + str(e) + '\n' + statement + '\n' + str(args))
        reinsert(query,curr,logger)
    except Exception as e:
        logger.error("Exception Error" + '\n' + str(type(e)) + '\n' + str(e) + '\n' + statement + '\n' + str(args))
        pass

def reinsert(query,curr,logger):
    statement = query[0].lower()
    args = list(query[1])
    insert = False
    if "insert into http_requests" in statement:
        stat_del = "delete from http_requests where request_id={} and site_id={} and link_id={}".format(args[-3],args[-2],args[-1])
        insert = True  
    if "insert into http_responses" in statement:
        stat_del = "delete from http_requests where response_id={} and site_id={} and link_id={}".format(args[-3],args[-2],args[-1]) 
        insert = True  
    if "insert into cookies" in statement:
        stat_del = "delete from cookies where cookie_id={} and site_id={} and link_id={}".format(args[-3],args[-2],args[-1]) 
        insert = True
    if insert == True:
        logger.info(stat_del)
        curr.execute(stat_del) 
        logger.info("reinsert")
        process_query(query,curr,logger) 
                


def drain_queue(sock_queue, curr, logger):
    """ Ensures queue is empty before closing """
    time.sleep(3)  # TODO: the socket needs a better way of closing
    while not sock_queue.empty():
        query = sock_queue.get()
        process_query(query, curr, logger)
