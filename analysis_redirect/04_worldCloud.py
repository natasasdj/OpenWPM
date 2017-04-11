"""
Minimal Example
===============
"""
import os
from wordcloud import WordCloud

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
keys_file = open(os.path.join(output_dir, 'keys'))

# Read the whole text
text = keys_file.read()
text.


# Generate a word cloud image
wordcloud = WordCloud().generate(text)


# Display the generated image:
# the matplotlib way:
fig_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/figs'
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)

import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(fig_dir, 'keys_worldCloud.png'))
plt.show()

keys_file.close()
