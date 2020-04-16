'''read the methylKit file, split it by chromosome'''

import sys
args = sys.argv
f = args[1]
print(args)
sample = f.split('.')[0]
context = f.split('.')[2][-3:]
print('input file: %s' % f)
print('sample: %s' % sample)
print('context: %s' % context)

with open(f,) as input:
	with open(sample+'_'+context+'a.methylKit', 'w') as a, open(sample+'_'+context+'b.methylKit', 'w') as b, open(sample+'_'+context+'c.methylKit', 'w') as c, open(sample+'_'+context+'d.methylKit', 'w') as d, open(sample+'_'+context+'e.methylKit', 'w') as e, open(sample+'_'+context+'f.methylKit', 'w') as f:
		for lines in input:
			if lines.startswith("chrBase"):
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
				if col[1] in ['arahy.Tifrunner.gnm1.Arahy.01', 'arahy.Tifrunner.gnm1.Arahy.02', 'arahy.Tifrunner.gnm1.Arahy.03','arahy.Tifrunner.gnm1.Arahy.04']:
					a.write(lines)
				elif col[1] in ['arahy.Tifrunner.gnm1.Arahy.05', 'arahy.Tifrunner.gnm1.Arahy.06', 'arahy.Tifrunner.gnm1.Arahy.07','arahy.Tifrunner.gnm1.Arahy.08']:
					b.write(lines)
				elif col[1] in ['arahy.Tifrunner.gnm1.Arahy.09', 'arahy.Tifrunner.gnm1.Arahy.10', 'arahy.Tifrunner.gnm1.Arahy.11','arahy.Tifrunner.gnm1.Arahy.12']:
					c.write(lines)
				elif col[1] in ['arahy.Tifrunner.gnm1.Arahy.13', 'arahy.Tifrunner.gnm1.Arahy.14', 'arahy.Tifrunner.gnm1.Arahy.15','arahy.Tifrunner.gnm1.Arahy.16']:
					d.write(lines)
				elif col[1] in ['arahy.Tifrunner.gnm1.Arahy.17', 'arahy.Tifrunner.gnm1.Arahy.18', 'arahy.Tifrunner.gnm1.Arahy.19','arahy.Tifrunner.gnm1.Arahy.20']:
					e.write(lines)
				elif col[1].startswith("arahy.Tifrunner.gnm1.scaffold"):
					f.write(lines)