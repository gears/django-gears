import re


header_re = r'^(\s*((/\*.*?\*/)|(//[^\n]*\n?)+))+'

header_1 = """
/* JavaScript file
 *

 *= require application
 */

// Header comment with other style
//= require test

/* Another header comment
 *
 *= require backbone
 */

function (){};

/* Not a header comment
 *
 *= require underscore
 */
"""

header_2 = """
function (){};
"""

print repr(re.match(header_re, header_1, re.DOTALL).group(0))
print repr(re.match(header_re, header_2, re.DOTALL).group(0))
