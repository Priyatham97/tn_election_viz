import re
import string
import pandas as pd

def preprocess(text, stopwords=None):

    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    # Removing Punctuation
    text = text.translate(text.maketrans('', '', string.punctuation))
    # remove all single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    # Removing extra-spaces
    text = re.sub(' +', ' ', text)
    text = text.replace('\n', ' ')
    return text.strip()


def get_alliance(partyname, year):
    alliance_dict = {
        "2016": ["INC", "IUML", "PT",
                 "MAMAK", "PTMK", "TNPWP"],
        "2019": ["INC", "CPI",
                 "CPM", "VCK", "IUML", "IJK", "KMDK",
                 "MDMK"],
        "2021": ["INC", "CPM", "VCK", "CPI", "MDMK", "IUML", "KMDK", "MMK",
                 "AIFB", "TVK", "MVK", "ATP"]
    }
    opposition_alliance = {
        "2021":["PMK","BJP","TMC","PTMK","TMMK","MMK","AIMMK","PBK","PDK"]
    }

    if partyname in alliance_dict[year]:
        return "DMK+"
    if partyname in opposition_alliance[year]:
        return "AIADMK+"

    return partyname

def get_total_voters(consti_no):
    return voters_map[consti_no]
    
if __name__ == '__main__':

    voters_df = pd.read_excel('./total_voter_count.xlsx')
    voters_map = voters_df.set_index('Constituency Number').to_dict()['Total Voters']
