# https://gist.github.com/bradmerlin/5693904

class Slice(object):
    def __init__(self, root, leng):
        self.root = root 
        # The original word
        self.leng = leng
        # How many morphemes should be used as the prefix for the new portmanteau
        self.morphemes = []
        self.output = '' #
        self.slice()

    def slice(self):
        import re
        ex = r'([^aeiou]*[aeiou]*)|[aeiou]*[^aeiou]*[aeiou]*'
        #ex = r'[^aeiou]*[aeiou]*[^aeiou]*|[aeiou]*[^aeiou]'
        root = self.root

		# Full list of morphemes for future use
        while root != '':
            end = re.match(ex, root).end()
            self.morphemes.append(root[0:end])
            root = root[end:]

		# Check that the number given isnt more than is available
        if len(self.morphemes) < self.leng:
            self.leng = len(self.morphemes)

		#Stitch together the output word
        g = 0
        while g < self.leng :
            self.output += self.morphemes[g]
            g += 1