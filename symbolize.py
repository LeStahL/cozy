# Tunguska by Team210 - 64k intro by Team210 at Solskogen 2k19
# Copyright (C) 2018  Alexander Kraus <nr4@z10.info>
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

import os
import argparse

from importlib.machinery import SourceFileLoader

Rule = SourceFileLoader("Rule", "minification/Rule.py").load_module()
Token = SourceFileLoader("Token", "minification/Token.py").load_module()
GLSLLexer130 = SourceFileLoader("GLSLLexer130", "minification/GLSLLexer130.py").load_module()
Compressor = SourceFileLoader("Compressor", "minification/Compressor.py").load_module()

# Parse command line args
parser = argparse.ArgumentParser(description='Team210 symbol packer.')
parser.add_argument('-o', '--output', dest='out')
args, rest = parser.parse_known_args()

if rest == []:
    print("Error: No input files present.")
    exit()

if rest == []:
    print("No input files. Will exit.")
    exit()
    
file = rest[0]
fragname = rest[0].split('\\')[-1].split('/')[-1].replace('.frag','').replace(".","").replace("\\","")
input_source = "const char *" + fragname + "_source = \""
with open(file, "rt") as f:
    input_source_ = f.read();
input_source += Compressor.compress(input_source_).replace('\"','\\\"').replace('\n', '\\n\"\n\"').replace('#version 130', '#version 130\\n') + "\\0"
input_source += "\";"

# Write output to file or stdout
if args.out == None:
    print(input_source)
else:
    with open(args.out, "wt", newline='\n') as f:
        f.write(input_source)
        f.close()
