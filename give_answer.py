import unicodedata
import wolframalpha
from nltk import word_tokenize, pos_tag, ne_chunk, conlltags2tree, tree2conlltags
import google
import wikipedia
import collections

#===============================================================#================================================================
# Classifying the type of question i.e location, date, person ,definiton
def classify_question(question):
    q = question.lower().split()
    
    if q[0] == 'where':
        return 'Location'
    elif 'year'  in question:
            return 'Date'
    elif 'country' in question:
        return 'Country'
    elif q[0] == 'who':
        return 'Person'
    elif q[0] == 'what':
        return 'Definition'
    else:

        return 'None'

#===============================================================
###########################################################################
# performing google search
def google_search(question):
    first_page = google.search(question,1)
    
    top_three_result = []
    i = 0
    while i<5:
        top_three_result.append(first_page[i].description)
        i+=1

    first_search = ''.join(top_three_result).encode('ascii','replace')
    

    ne_tree = (ne_chunk(pos_tag(word_tokenize(first_search))))

    iob_tagged = tree2conlltags(ne_tree)

    ss = [tuple(map(str,eachTuple)) for eachTuple in iob_tagged]
    question_type = classify_question(question)
    print ('question_type: ',question_type)
    if question_type == 'None':
        ans = "Oops! I don't know."
    else:
        google_answer = []
        if question_type == 'Person':
            for i in range(len(ss)):
                if ss[i][2] == 'B-PERSON'or ss[i][2] == 'I-PERSON':
                    google_answer.append(ss[i][0])
        elif question_type == 'Country':
            print ('country identified')
            for i in range(len(ss)):
                if ss[i][2] == 'B-GPE'or ss[i][2] == 'I-GPE':
                    google_answer.append(ss[i][0])
        elif question_type == 'Location':
            for i in range(len(ss)):
                if ss[i][2] == 'B-LOCATION'or ss[i][2] == 'I-LOCATION':
                    google_answer.append(ss[i][0])
        elif question_type == 'Date':
            for i in range(len(ss)):
                if ss[i][2] == 'B-DATE'or ss[i][2] == 'I-DATE':
                    google_answer.append(ss[i][0])
        print ('google: ',google_answer)
        if not google_answer:
            ans = "Oops, I don't know! "
        else:
            print ('inside else')
            counts = collections.Counter(google_answer)
            print ('counts: ',counts)
            t = counts.most_common(4)
            candidate_answer =  [ seq[0] for seq in t ]
            print (candidate_answer)
            
            for i in range(len(candidate_answer)):
                candidate_answer[i] = 'Candidate Answer '+ str(i+1)+' '+ candidate_answer[i]
            candidate_answer = '\n'.join(candidate_answer)
            ans = candidate_answer
    return ans

##################################################################################


def answer_question(question):
    try:
        
        if ans == 'None':
            print ('ans is none')
            q_type = classify_question(question)
            if q_type == 'Definition' or q_type == 'Location':
                app_id = '9W2L7P-YTY39WTEAH'   
                if not app_id:
                    
                    client = wolframalpha.Client(app_id)
                    res = client.query(question)
                    print ('ans is who')
                    ans = str(next(res.results).text).replace('.', '.\n')

                              
            
            
            
            else:
                print ('none-google')
                ans = google_search(question)
                print ('google answ: ',ans)

        return ans

    except:
        try:
            print ('Exception at first run')
            q_type = classify_question(question)
            if q_type == 'Definition' or q_type == 'Location':
                print ('inside-wiki')
                ans = google_search(question)
                
            
            
            
            else:
                print ('inside-google')
                ans = google_search(question)
                print ('google answ: ',ans)

            return ans
        except:
               return "Sorry! I don't know. Please try something else!"

