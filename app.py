from flask import *  
import json
from xml.dom import minidom

def svg_parse(name):
    ## Parse File into lists
    doc = minidom.parse(name)  # enter file name
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]

    path_labels = [path.getAttribute('inkscape:label') for path
                    in doc.getElementsByTagName('path')]

	width = [path.getAttribute('width') for path
                in doc.getElementsByTagName('svg')]

	height = [path.getAttribute('height') for path
					in doc.getElementsByTagName('svg')]

	transform = [path.getAttribute('transform') for path
					in doc.getElementsByTagName('g')]

    doc.unlink()

	if not transform:
    transform = [0,0]
	viewbox = []
	viewbox.append(transform[0])
	viewbox.append(transform[1])
	viewbox.append(width[0])
	viewbox.append(height[0])
	viewbox = [' '.join([str(x) for x in viewbox])]

    #build the dic
    foo = []

    for row in range(len(path_strings)):
        d = {'type':'path',
            'fill':{
                'paint':'none'
                },
            'stroke':{
                'paint':'#999999',
                'width':'05'
                },
            'style':{},
            'd':path_strings[row],
            'name':path_labels[row]
            }
        foo.append(d)
		
	header = {'type':'ia.shapes.svg',
          'version':'0',
          'props':{
              'viewbox':viewbox[0],
              'preserveAspectRatio':'xMinYmin',
              'elements':{},
              'style':{}
              },
          'meta':{
              'name':'MAP'
              },
          'position':{
              'x':0,
              'y':0,
              'height':float(height[0]),
              'width':float(width[0])
              },
          'custom':{}
          }

	header['props']['elements'] = foo
	header = [header]
	
    ## Export to JSON
    j = json.dumps(header, indent=4)
    f = open('output.json', 'w') #output file name
    print(j,file=f)
    f.close()
	

app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  

#Parse for Map SVG
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        svg_parse(f.filename)
        #return render_template("success.html", name = f.filename)
        return send_file('output.json', as_attachment=True)

#Parse for SLD SVG
@app.route('/success_2', methods = ['POST'])  
def success_2():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        svg_parse(f.filename)
        #return render_template("success.html", name = f.filename)
        return send_file('output.json', as_attachment=True)

if __name__ == '__main__':  
    app.run(debug = True)  
