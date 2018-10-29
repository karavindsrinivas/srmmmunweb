from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import re
import pandas as pd;
from collections import Counter
import operator
import warnings
import json
import pickle

warnings.filterwarnings("ignore");
sw2=['chair', 'best', 'secretary', 'highcommendation', 'journalist', 'specialmention2', 'diplomacy', 'honmen', 'highcom', 'comm.', 'deputy', 'specialmention1', 'chairs', 'young', 'no', 'participate', 'director', 'honorablemention', 'highcomm', '2nd', 'runner', 'declared', 'honorable', 'commendable', 'commendation', 'not', 'of', 'most', 'honanary', 'awards', 'judge', 'fspa', 'participant', 'still', 'bd', 'letter', 'saudi', 'srm', 'republic', 'hon', 'photographer', 'merit', 'opening', 'vice', 'mentions', 'ssn', 'speech', 'comm', 'hindustan', 'about', 'high', 'verbalmention', 'honorary', 'reporter', 'honourable', 'papers', 'commission', 'junction', 'compensation', 'outstanding', 'photojournalist', 'com', 'press', 'paper', 'rapporteur', 'speaker', 'hylc', 'prize', 'pariticipation', 'oc', 'ongoing', 'nil', 'model', 'delegate', 'member','award', 'nan', 'verbalmentions', 'member', 'none', 'first', 'held', 'yet', 'del', 'verbal', 'spec', 'special', 'mntn', 'spcl', 'spc', 'mun', 'men', '3rd', 'delegation', 'chairperson', 'specmen', 'honourableâ€', 'up', 'promising', 'mention', 'fps', 'general', 'position', 'leadership','vit','vellore','vitc','vitness','chennai','college','slcu','jadavpur','kiit','iit','bits','executive','organizing','volunteer']


app=Flask(__name__)
CORS(app);

@app.route('/')
def form():
    d = {"1": "hello"}
    return jsonify(d)

@app.route('/recd',methods=['GET','POST'])
def recd():
    if request.method=='GET': 
        x = request.args.get('name');
        return('hello');
        x=' '.join(x.split());
        x=x.lower();
        x=re.sub('[^A-Za-z0-9]+', ' ', x)
        x=x.split();

        #MAKE THE DOCUMENT ONLY THE LIST OF KEYWORDS
        c=[]
        for i in range(0,len(x)):
            if(x[i]=="model"):
                x[i]=x[i+1]=x[i+2]="";
            elif x[i]=="mun" or "mun" in x[i]:
                x[i]="";
            if(x[i].isnumeric()):
                x[i]="";
            x[i]=re.sub("[^a-zA-Z0-9]+", "", x[i])
            if(x[i]!=""):
                c.append(x[i]);
        ct = [t for t in c if (re.match(r'[^\W]*$', t) or ('&' in t)==True)]
        pickle_in=open("sws.pickle","rb");
        stopwords=pickle.load(pickle_in)
        pickle_in.close();
        c= [t for t in ct if t not in stopwords]
        pickle_in=open("dict23.pickle","rb");
        s=pickle.load(pickle_in)
        pickle_in.close();

        #GET COMMITTEE NAMES
        ct=[]
        st="";
        skip=0;
        for i in range(0,len(c)):
            if skip!=0:
                skip=skip-1;
                continue;
            if(st==""):
                st=str(c[i]);
                for j in range(i+1,len(c)+1):
                    if st in s.keys():
                        ct.append(s[st])
                        skip=len(st.split())-1;
                        st="";
                        if(j==len(c)-1):
                            skip=1;
                        break;
                    else:
                        if(len(st.split())==6 or j>len(c)-1):                
                            skip=0;
                            st="";
                            break;
                        else:
                            st=st+" "+str(c[j])
        #GETTING 
        ct=Counter(ct);
        sx=sorted(ct.items(),reverse=True,key=operator.itemgetter(1))
        v=sum(ct.values())
        
        pickle_in=open("pickle23.pickle","rb");
        df2=pickle.load(pickle_in)
        pickle_in.close();
        print(df2);
        x=[]
        cols=[]
        for i in sx:
            cols.append(i[0]);
            val=df2[i[0]]*i[1]/v;
            x.append(val);
            
        df3=pd.DataFrame.from_items([(s.name,s) for s in x])
        df3['soln']=0
        for i in sx:
            df3['soln']=df3['soln']+df3[i[0]]
        df4=pd.DataFrame(df3['soln'])
        a=sum(df4['soln'])
        df4['soln']=df4['soln']*100/a;
        df5=(df4.nlargest(4,'soln')).T
        l=df5.columns.values;
        xk=dict()
        val=0;
        for i in l:
            xk[val]=i;
            val+=1;
        ans=json.dumps(xk);
        return ans;
                               
if __name__=="__main__":
    app.run(debug=True) 
