from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from multi_rake import Rake
import spacy
from lxml import html
from lxml.html.clean import clean_html
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.stem import PorterStemmer
#import nltk
#nltk.download('punkt')

class MySpider(CrawlSpider):
       
       name = 'crawlspider'
       allowed_domains = ['afro.who.int']
       start_urls = ['https://www.afro.who.int/health-topics/coronavirus-covid-19']
       rules = (
           Rule(LinkExtractor(), callback='parse_item', follow=True),
       )
       rake = Rake(max_words_unknown_lang=3)
       j_africa = ['africa','nigeria','ethiopia','egypt','congo','tanzania','kenya','uganda','algeria','sudan','morocco',
                   'mozambique','ghana','angola','somalia','ivory coast','madagascar','cameroon','burkina','niger','malawi',
                   'zambia','mali','senegal','zimbabwe','chad','tunisia','guinea','rwanda','benin','burundi','sudan','eritrea',
                   'sierra', 'leone','togo','libya','Mauritania','liberia','namibia','botswana','lesotho','gambia','gabon',
                   'guinea-bissau','mauritius','Guinea','eswatini','djibouti','comoros','cape','verde','seychelles','tomé']
       
       j_covid = ['covid-19','coronavirus']
       
       def occurence(self,liste):
              liste_uniq = list(set(liste))
              maliste = []
              for elt in liste_uniq:
                     maliste.append((elt,liste.count(elt)))
              return maliste
       
       def get_keywordSpacy(self,text):
              nlp = spacy.load('en')
              keywords = []
              pos_tag = ['PROPN','NOUN']
              doc = nlp(text.lower())
              for token in doc:
                     if(token.pos_ in pos_tag):
                            keywords.append(token.text)
              return keywords
              
       def decideurSpacy(self,textSpacy,jargon):
              decision = 0
              list_covid = [val for val in textSpacy if val in jargon[0]]
              list_afro = [val for val in textSpacy if val in jargon[1]]
              if(len(list_covid)> 0 and len(list_afro)> 0):
                     decision = 1
              return decision

       def stemSentence(self,sentence):
              porter = PorterStemmer()
              token_words = word_tokenize(sentence)
              
              stem_sentence=[]

              for word in token_words:
                     new_word = porter.stem(word)
                     if len(new_word)> 2:
                            stem_sentence.append(new_word)
                            stem_sentence.append(" ")
              return " ".join(stem_sentence)
              

       def parse_item(self, response):
           item = dict()
           #item['title'] = response.meta['link_text']
           imageDomain = self.start_urls[0].rsplit('/')
           imageSrc = response.css('img').xpath('@src').getall()
           mesimg = []
           #html = urlopen(response.url).read()
           #soup = BeautifulSoup(html)
           #urlopen(response.url).close()
           for img in imageSrc:
               if img.startswith("http"):
                   # start with http, therefore take this as the full link
                   # on ajoute directement le lien dans la liste car on a le chemin absolue de l'image
                   mesimg.append(img)
               # on recupere le nom de domaine d'abord et le reste du lien  avant d'ajouter dans la liste ,car on a un chemin absolue
               else:
                   # does not start with http, therefore construct the full url from the base url plus the absolute image link
                   # str(imageDomain[0]) <=> https:
                   mesimg.append(str(imageDomain[0]) + "//" + str(imageDomain[2]) + str(img))
           # extracting basic body
           
           videos = response.css('div').xpath('@data-video-embed-field-modal').getall()
           mesVideos = []
           for video in videos:
               vide = '<iframe' + video.split('<iframe')[1].split('</iframe>')[0] + '</iframe>'
               mesVideos.append(vide)
           mesVideos = list(set(mesVideos))
           #gerer le texte debut

           # kill all script and style elements
           #for script in soup(["script", "style"]):
                  #script.extract()    # rip it out

           # get text
           #text = soup.get_text()

           # break into lines and remove leading and trailing space on each
           #lines = (line.strip() for line in text.splitlines())
           # break multi-headlines into a line each
           #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
           # drop blank lines
           #text = '   '.join(chunk for chunk in chunks if chunk)



           #fin

           
           #body = '\n'.join(response.xpath('//body//text()[re:test(.,"w+")]').extract()).replace("\n","")
           s = response.xpath('//body').extract_first()
           tree = html.fromstring(s)
           texte = ''.join(clean_html(tree).text_content().strip()).replace("\n","").replace("\t","")
           #texte = (clean_html(tree).text_content().strip()).replace("\n"," ").replace("\t"," ")
           #texte = (clean_html(tree).text_content()).replace(r"\u"," ").replace("\n"," ").replace("\t"," ")
           #texte = (clean_html(tree))
           #texte = re.sub('\s\s+'," . ",texte)
           #keywords = self.rake.apply(texte.lower())
           texte = self.stemSentence(texte)
           bodySpacy = self.get_keywordSpacy(texte)
           #if self.decideurSpacy(bodySpacy,[self.j_covid,self.j_africa]) == 1:                 
                  #item['url'] = response.url
                  #item['bodyRake'] = list(set([x[0] for x in keywords]))
                  #item['bodySpacy'] = list(set(self.get_keywordSpacy(body)))
                  #item['body'] = body
                  #item['img'] = mesimg
                  #item['videos'] = mesVideos
                  # or better just save whole source
                  #item['source'] = response.body
           item['bodySpacy'] = self.occurence(bodySpacy)
           #item['bodySpacy'] = texte 
           #item['bodyRake'] = keywords
           return item
