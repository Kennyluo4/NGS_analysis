'''read the dss file, split it by chromosome'''

import sys
args = sys.argv
f = args[1]
print(args)
sample = f.split('_')[0]
context = f.split('.')[0][-3:]
print('input file: %s' % f)
print('sample: %s' % sample)
print('context: %s' % context)
lnum = 0
num1 = 0
num2 = 0
num3 = 0
num4 = 0
num5 = 0
num6 = 0
num7 = 0

with open(f,) as input:
	with open(sample+'_'+context+'.dss.a', 'w') as a, open(sample+'_'+context+'dss.b', 'w') as b, open(sample+'_'+context+'dss.c', 'w') as c, open(sample+'_'+context+'dss.d', 'w') as d, open(sample+'_'+context+'dss.e', 'w') as e, open(sample+'_'+context+'dss.f', 'w') as f:
		for lines in input:
			lnum += 1
			if lines.startswith("chr"):
				header = lines
				a.write(header)
				b.write(header)
				c.write(header)
				d.write(header)
				e.write(header)
				f.write(header)
				continue
			else:
				col = lines.strip().split('\t')
				if col[0] in ['arahy.Tifrunner.gnm1.Arahy.01', 'arahy.Tifrunner.gnm1.Arahy.02', 'arahy.Tifrunner.gnm1.Arahy.03','arahy.Tifrunner.gnm1.Arahy.04']:
					a.write(lines)
					num1 += 1
				elif col[0] in ['arahy.Tifrunner.gnm1.Arahy.05', 'arahy.Tifrunner.gnm1.Arahy.06', 'arahy.Tifrunner.gnm1.Arahy.07','arahy.Tifrunner.gnm1.Arahy.08']:
					b.write(lines)
					num2 += 1
				elif col[0] in ['arahy.Tifrunner.gnm1.Arahy.09', 'arahy.Tifrunner.gnm1.Arahy.10', 'arahy.Tifrunner.gnm1.Arahy.11','arahy.Tifrunner.gnm1.Arahy.12']:
					c.write(lines)
					num3 += 1
				elif col[0] in ['arahy.Tifrunner.gnm1.Arahy.13', 'arahy.Tifrunner.gnm1.Arahy.14', 'arahy.Tifrunner.gnm1.Arahy.15','arahy.Tifrunner.gnm1.Arahy.16']:
					d.write(lines)
					num5 += 1
				elif col[0] in ['arahy.Tifrunner.gnm1.Arahy.17', 'arahy.Tifrunner.gnm1.Arahy.18', 'arahy.Tifrunner.gnm1.Arahy.19','arahy.Tifrunner.gnm1.Arahy.20']:
					e.write(lines)
					num6 += 1
				elif col[0].startswith("arahy.Tifrunner.gnm1.scaffold"):
					f.write(lines)
					num7 += 1
writeline = num1 + num2 + num3 + num4 + num5 + num6 + num7   
  
print("Total line: %s, write to files: %s" % (lnum, writeline))