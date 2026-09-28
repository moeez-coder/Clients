from aiark import *
PH=["CAD to render","CAD rendering","CGI product","product CGI","product rendering","3D product rendering","product visualization","product visualisation","photorealistic rendering","3D product animation","industrial CGI","technical animation","industrial animation","product animation","3D product visualization","CGI studio","CGI agency"]
src=[{"mode":"WORD","source":s} for s in ("DESCRIPTION","SEO","KEYWORD")]
body={"size":100,"account":{"keyword":{"any":{"include":{"sources":src,"content":PH},"exclude":{"sources":src,"content":["architectural visualization","architectural rendering","archviz","real estate rendering","interior rendering","BIM"]}}}}}
import sys; pull(body,int(sys.argv[1]),'aiark_q1.json')
