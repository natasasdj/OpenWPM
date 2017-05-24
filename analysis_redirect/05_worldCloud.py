"""
Minimal Example
===============
"""
import os
import sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt

input_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/'
input_file = sys.argv[1]
keys_file = open(sys.argv[1])

#keys_file = open(file)

# Read the whole text
text = keys_file.read()
print text


# Generate a word cloud image
#wordcloud = WordCloud().generate(text)


# Display the generated image:
# the matplotlib way:
fig_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/figs'
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)


#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40,collocations=False).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(fig_dir, output_file) + '.png'))
plt.show()

keys_file.close()
