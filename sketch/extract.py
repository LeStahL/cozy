# Hardcyber - PC-64k-Intro by Team210 at Deadline 2k19
# Copyright (C) 2019  Alexander Kraus <nr4@z10.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from svgpathtools import Path, Line
from svgpathtools import parse_path

path_string = 'M 70.710938 125.5 L 70.710938 396.2207 L 268.21289 396.2207 L 268.21289 125.5 L 182.31836 125.5 L 182.31836 284.61523 L 204.05078 284.61523 L 204.05078 299.73438 L 144.44922 299.73438 L 144.44922 284.61523 L 167.19922 284.61523 L 167.19922 125.5 L 70.710938 125.5 z M 283.33203 125.5 L 283.33203 396.2207 L 337.86914 396.2207 L 337.86914 219.44141 L 352.98633 219.44141 L 352.98633 396.2207 L 477.3125 396.2207 L 477.3125 125.5 L 421.7793 125.5 L 421.7793 292.17578 L 406.66016 292.17578 L 406.66016 125.5 L 283.33203 125.5 z M 492.43164 125.5 L 492.43164 396.2207 L 691.95508 396.2207 L 691.95508 258.31445 L 585.36914 258.31445 L 585.36914 292.17578 L 570.25195 292.17578 L 570.25195 219.44141 L 585.36914 219.44141 L 585.36914 243.19727 L 691.95508 243.19727 L 691.95508 125.5 L 492.43164 125.5 z'

path = parse_path(path_string)

# find dimensions
xmax = -1.e9
xmin = 1.e9
ymax = -1.e9
ymin = 1.e9
for line in path:
    xmax = max(xmax, line.start.real)
    xmax = max(xmax, line.end.real)
    
    xmin = min(xmin, line.start.real)
    xmin = min(xmin, line.end.real)
    
    ymax = max(ymax, line.start.imag)
    ymax = max(ymax, line.end.imag)
    
    ymin = min(ymin, line.start.imag)
    ymin = min(ymin, line.end.imag)

# rescale path
for i in range(len(path)):
    path[i].start -= complex(xmin,ymin)
    path[i].start = complex(path[i].start.real/abs(xmax-xmin), path[i].start.imag/abs(ymax-ymin)/100.*29.)
    path[i].start -= complex(.5,.5*29./100.)
    path[i].start = complex(path[i].start.real,-path[i].start.imag)
    
    path[i].end -= complex(xmin,ymin)
    path[i].end = complex(path[i].end.real/abs(xmax-xmin), path[i].end.imag/abs(ymax-ymin)/100.*29.)
    path[i].end -= complex(.5,.5*29./100.)
    path[i].end = complex(path[i].end.real,-path[i].end.imag)

# sort path
#newpath = [ path[0] ]
#del path[0]
#while len(path) > 1:
    #print(len(path))
    #for j in range(len(path)-1):
        #print(j,"/",len(path))
        #if abs(newpath[-1].end - path[j].start)<5.e-1:
            #newpath += [ path[j] ]
            #del path[j]
            #break
#path = newpath
    
with open('unc.frag', 'wt') as f:
    f.write('const int npts = ' + str(4*len(path)) + ';\n')
    f.write('const float path[npts] = float[npts](')
    
    for i in range(len(path)-1):
        line = path[i]
        f.write('{:.3f}'.format(line.start.real) + ',' + '{:.3f}'.format(line.start.imag) + ',')
        f.write('{:.3f}'.format(line.end.real) + ',' + '{:.3f}'.format(line.end.imag) + ',')
    line = path[-1]
    f.write('{:.3f}'.format(line.start.real) + ',' + '{:.3f}'.format(line.start.imag) + ',')
    f.write('{:.3f}'.format(line.end.real) + ',' + '{:.3f}'.format(line.end.imag))
    f.write(');\n')
    f.close()
