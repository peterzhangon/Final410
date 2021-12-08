from flask import Flask
from flask import render_template, request, jsonify
from flask_cors import CORS
import json
import os
import metapy
import requests
import base64
import sys
import re


app = Flask(__name__) 
cors = CORS(app)
environ = 'development'
dataconfig = json.loads(open("config.json", "r").read())
app.dataenv = dataconfig[environ]
app.rootpath = dataconfig[environ]["rootpath"]
app.datasetpath = dataconfig[environ]['datasetpath']
app.searchconfig = dataconfig[environ]['searchconfig']
index = metapy.index.make_inverted_index(app.searchconfig)
query = metapy.index.Document()
uni_list = json.loads(open(dataconfig[environ]["unispath"],'r').read())["unis"]
loc_list = json.loads(open(dataconfig[environ]["locspath"],'r').read())["locs"]


@app.route('/')
def home():
    return render_template('index.html',uni_list= uni_list,loc_list=loc_list)

@app.route('/admin')
def admin():
    return render_template('admin.html')

def filtered_results(results,num_results,min_score,selected_uni_filters,selected_loc_filters):
    filtered_results = []
    universities = []
    states =[]
    countries = []
    res_cnt = 0
    # print (selected_uni_filters,selected_loc_filters)
    for res in results:
        university = index.metadata(res[0]).get('university')
        state = index.metadata(res[0]).get('state')
        country = index.metadata(res[0]).get('country') 
        print(" --begin-------------- line_49")
        print("filter res[0]:", res[0])
        print("filter res[1]:", res[1])
        print("index.metadata(res[0]):", type(index.metadata(res[0])))
        # ('filter res[0]:', 6086L) ------------------- index
        # ('filter res[1]:', 0.3868231773376465) ------ score
        print(" --end-------------- line_49")
        if (res[1]>min_score) and (state in selected_loc_filters or country in selected_loc_filters) and (university in selected_uni_filters) :
            filtered_results.append(res)
            res_cnt += 1
            universities.append(university)
            states.append(state)
            countries.append(country)
            if res_cnt == num_results:
                break
    print(" --begin-------------- line_58")
    print("filtered_results:", filtered_results)
    print("universities:", universities)
    print("states:", states)
    print("countries:", countries)
    print(" --end-------------- line_58")
    return filtered_results,universities,states,countries

@app.route('/search', methods=['POST'])
def search():
    data = json.loads(request.data)
    querytext = data['query']
    num_results = data['num_results']
    selected_loc_filters = data['selected_loc_filters']
    selected_uni_filters = data['selected_uni_filters']

    query = metapy.index.Document()
    query.content(querytext)
    min_score = 0.01

    # Dynamically load the ranker
    sys.path.append(app.rootpath + "/expertsearch")

    from ranker import load_ranker

    ranker = load_ranker(app.searchconfig)

    results = ranker.score(index, query, 100) 

    results,universities,states,countries = filtered_results(results,num_results,min_score,selected_uni_filters,selected_loc_filters)
    print("*******begin**************** line_96");
    print("results size:", len(results))
    print("results contents:", str(results))
    print("results[0]", results[0])
    print("results[1]", results[1])
    print("results[2]", results[2])
    print("results[3]", results[3])
    print("results[4]", results[4])
    print("*******end**************** line_96");
    doc_names = [index.metadata(res[0]).get('doc_name') for res in results]
    depts = [index.metadata(res[0]).get('department') for res in results]
    fac_names = [index.metadata(res[0]).get('fac_name') for res in results]
    fac_urls = [index.metadata(res[0]).get('fac_url') for res in results]

    previews = _get_doc_previews(doc_names, querytext)
    emails = [index.metadata(res[0]).get('email') for res in results]
    phones = [index.metadata(res[0]).get('phone') for res in results]
    print("++++++++++++++++++++++");
    print("\n\n previews:", previews)
    print("\n\n emails:", emails)
    print("\n\n phones:", phones)
    print("\n\n fac_names:", fac_names)

    print("++++++++++++++++++++++");
    docs = list(zip(doc_names, previews, emails, universities,depts, fac_names,fac_urls,states,countries, phones))
    print("\n\n docs:", docs)
    print("\n\n docs[0]:", docs[0])
    print("\n\n docs[1]:", docs[1])
    print("\n\n docs[2]:", docs[2])

    return jsonify({
        "docs": docs
    })



@app.route("/admin/ranker/get")
def get_ranker():
    ranker_path = app.rootpath + "/expertsearch/ranker.py"
    ranker_contents = open(ranker_path, 'r').read()

    return jsonify({
        "ranker_contents": ranker_contents
    })

@app.route("/admin/ranker/set", methods=["POST"])
def set_ranker():
    data = json.loads(request.data)

    projectId = data["projectId"]
    apiToken = data["apiToken"]

    ranker_url = "https://lab.textdata.org/api/v4/projects/" + projectId + "/repository/files/search_eval.py?ref=master&private_token=" + apiToken
    resp = requests.get(ranker_url)

    gitlab_resp = json.loads(resp.content)
    file_content = gitlab_resp["content"]
    ranker_path = app.rootpath + "/expertsearch/ranker.py"

    with open(ranker_path, 'wb') as f:
        f.write(base64.b64decode(file_content))
        f.close()

    return "200"

def _get_doc_previews(doc_names,querytext):
    return list(map(lambda d: _get_preview(d,querytext), doc_names))

def format_string(matchobj):
    
    return '<b>'+matchobj.group(0)+'</b>'

def _get_preview(doc_name,querytext):
    preview = ""
    num_lines = 0
    preview_length = 2
    fullpath = app.datasetpath + "/" + doc_name

    with open(fullpath, 'r') as fp:
        while num_lines < preview_length:
            line = fp.readline()
            found_phrase = False
            if not line:
                break
            formatted_line = str(line.lower())
            for w in querytext.lower().split():

                (sub_str,cnt) = re.subn(re.compile(r"\b{}\b".format(w)),format_string,formatted_line)

                if cnt>0:
                    formatted_line = sub_str
                    found_phrase = True 

            if found_phrase:
                preview += formatted_line

                num_lines += 1
        fp.close()
 
    short_preview = ''
    prev_i = 0
    start = 0
    words = preview.split()
    cnt = 0
    i=0
   
    while i<len(words):
        

        
        if '<b>' in words[i]:
            start = min(i-prev_i,5)
            
            if  i-start>0:
                short_preview += '...'
            short_preview += ' '.join(words[i-start:i+5])
            i+=5
            prev_i = i
            cnt +=1
        else:
            i+=1
        if cnt==3:
            break


    return short_preview



if __name__ == '__main__':
    # environ = os.environ.get("APP_ENV")
    environ = 'development'
    dataconfig = json.loads(open("config.json", "r").read())
    app.dataenv = dataconfig[environ]
    app.rootpath = dataconfig[environ]["rootpath"]
    app.datasetpath = dataconfig[environ]['datasetpath']
    app.searchconfig = dataconfig[environ]['searchconfig']

    app.run(debug=True,threaded=True,host='localhost',port=8095)
