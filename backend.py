__author__ = 'zthorn'

import requests
#	#curl --data-urlencode query@query.xml http://central.biomart.org/martservice/results
from suds.client import Client
from flask import Flask
from flask import render_template
from flask import request

import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def getAttr():
    url = ""
    ds = ""
    cfg = ""
    res = ""
    list=""
    fil=""
    fillist=None
    if request.method == 'POST':
        url = request.form['url']
        url = url.replace(' ', '')
        list = url.split(',')

        fil = request.form['fil']
        fil = fil.replace(' ','')
        if fil is not "":
            fillist = fil.split(',')

        #"hsapiens_gene_ensembl"
        ds = request.form['ds']
        #"gene_ensembl_config"
        cfg = request.form['cfg']
        res = queryBiomart(ds,fillist,cfg,list)
    return render_template('index.html',attri=list, ds=ds, cfg = cfg, res = res )





def queryBiomart(dataset,filter,cfg,attr):
    client = Client("http://central.biomart.org/martsoap?wsdl")
    attribute=""
    fil=""
    if filter is not None:
        for i in filter:
            fil+='<Filter name="'+i+'" value="1" filter_list=""/>'

    for i in attr:
        attribute+='<Attribute name="'+i+'"/>'
    query = """
    <!DOCTYPE Query>
        <Query client="true" processor="TSV" limit="-1" header="1">
	        <Dataset name="%s" config="%s">
	            %s
                %s
	        </Dataset>
        </Query>""" % (dataset,cfg,fil,attribute)
    results = client.service.getResults(query)
    print ("Results are:\n" + results)
    print(results)
    return results

if __name__=="__main__":

    app.run()