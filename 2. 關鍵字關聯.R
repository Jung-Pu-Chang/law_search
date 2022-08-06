library(dplyr)
library(data.table) #fread dcast 
library(arules) #關聯分析包
library(arulesViz) 
library(DT) #dataframe 轉 html
library(htmlwidgets) #存出去

##clean####
data <- read.csv("D:\\國泰產\\temp\\final.csv",fileEncoding ="UTF-8")

#踢掉長度<2(大多為名字)
data <- subset(data, nchar(as.character(data$content_cut)) >= 2)

關聯格式 <- data %>%
  group_by(JID) %>% 
  mutate(row = row_number()) %>% 
  dcast(JID ~ row, value.var=c("content_cut"))

關聯格式 <- 關聯格式[,-c(1)]
關聯格式[is.na(關聯格式)] <- ""
write.table(關聯格式, file="D:\\國泰產\\temp\\關聯格式.csv", sep = ",", na = "", row.names=FALSE, col.names = TRUE)

##apriori####
trans <- read.transactions(file="D:\\國泰產\\temp\\關聯格式.csv",sep=",", rm.duplicates=TRUE)
rule1 <- apriori(trans,parameter = list(support = 0.01,confidence = 0.8,
                                        minlen=2,maxlen=5))
outcome <- data.frame(lhs = labels(lhs(rule1)),rhs = labels(rhs(rule1)),rule1@quality)
加指標 <- data.frame(interestMeasure(rule1, measure = c("chiSquared", "jaccard"), significance=T, data))
# coverage = 左邊品項占比
# 卡方 <0.05 拒絕 r^2=0
eda <- cbind(outcome,加指標)
eda <- subset(eda,chiSquared<0.05)
colnames(eda) <- c("content", "RHS","support","confidence","coverage","lift","count","Chi-square","jaccard") 
eda$content <- gsub("[{}]","",eda$content)
eda$RHS <- gsub("[{}]","",eda$RHS)
eda <- subset(eda,eda$content!=""&eda$RHS!="")
eda <- eda[,c(1,2,9)]
eda$support <- round(eda$support,2)
eda$jaccard <- round(eda$jaccard,2)
eda <- arrange(eda,desc(eda$jaccard))

#eda <- subset(eda, nchar(as.character(eda$content)) >= 30)


##dashboard####
p = datatable(eda,colnames = c('詞彙1','詞彙2','JC'),
              rownames = FALSE, width="100%",
              options = list(columnDefs = list(list(className = 'dt-center', targets = 0:4))))
saveWidget(p,"D:\\law_search_key.html", selfcontained = TRUE, libdir = NULL,
           background = "white")
