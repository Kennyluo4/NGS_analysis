##volcano plot
#DEG result file must end with 'result.csv'
library(ggplot2)
files <-list.files(pattern="result.csv")
for (i in 1:length(files)){
	data <- read.csv(files[i],header = T, row.names = 1)
	picname <- paste(gsub(".csv","",files[i]),".pdf")
	P <- data[,6]
	#FC <- data[,4]
	logFC = data[,2]
	df <- data.frame(P,logFC)
	df$threshold <- as.factor(abs(logFC)>1 & P <0.05)
	ggplot(df, aes(x=logFC, y = -log10(P), colour=threshold)) + geom_point(alpha=0.7, size=1) + xlab("log2 fold change") + ylab("-log10 p-value")+theme(legend.position='none')+ geom_vline(xintercept = c(-1,1)) + geom_hline(yintercept = -log10(0.05))
	ggsave(picname)
}
