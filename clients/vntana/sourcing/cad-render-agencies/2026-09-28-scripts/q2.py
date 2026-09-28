from aiark import *
SEEDS=[["https://www.linkedin.com/company/kinetic-vision","https://www.linkedin.com/company/ikarus3d","https://www.linkedin.com/company/3dexcite","https://www.linkedin.com/company/medialab-3d-solutions","https://www.linkedin.com/company/renderthat"],
       ["https://www.linkedin.com/company/moonshot-cgi","https://www.linkedin.com/company/run-for-the-hills","https://www.linkedin.com/company/whipsaw","https://www.linkedin.com/company/lavalabs-moving-images","https://www.linkedin.com/company/brickland-sweden"]]
IND=["advertising services","marketing services","design services","graphic design","animation and post-production","media production","photography"]
import sys
for i,s in enumerate(SEEDS):
    body={"size":100,"lookalikeDomains":s,"account":{"industries":{"any":{"include":{"mode":"WORD","content":IND}}}}}
    pull(body,int(sys.argv[1]),f'aiark_q2_{i}.json')
