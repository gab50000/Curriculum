#!/usr/bin/python

beginning="""\documentclass[11pt, a4paper]{moderncv}
\moderncvtheme{classic}
\moderncvcolor{green}
\usepackage[utf8]{inputenc}"""

name="\\name{%s}{%s}"
address = "\\address{%s}{%s}"
phone = "\\phone{%s}"
mobile ="\\mobile{%s}"
email = "\\email{%s}"
title ="\\title{%s}"
photo ="\\photo[3.5cm][0.4pt]{%s}" 

middle ="""\begin{document}

\makecvtitle"""

section = "\section{$sectiontitle}"
cventry = "\cventry{$from -- $to}{$what}{$name}{$where}{\\textit{$mark}}{}"
cvitem  = "\cvitem{$title}{$cvitemdescription}"
cvlistitem = "\cvlistitem{$cvlistitemdescription}"

ending = """\\recipient{%s}{%s}
\date{%s}
\opening{%s}
\closing{%s}
\makelettertitle
$story
\\newline\\newline
\makeletterclosing
\end{%s}"""

def generate(cvsections, cventries, cvlistitems, ):
	with open("../../private/cv.tex") as f:
		for cid in cvsections.keys():
			for cventry in cventries[cid]:
				print >> f, cventry.title, cventry.text
			for 
