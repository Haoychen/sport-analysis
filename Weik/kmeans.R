library(data.table)
library(dplyr)

event<- fread('event_info.csv')
event<- as.data.frame(event)
info<-select(event, player_id, game_id, type_id, outcome)
player<- read.csv('player_info.csv')
player$position<- as.vector(player$position)
player<- player[player$position!='Goalkeeper',]


k.data<- data.frame('id' = 0, 'Position' = 0, 'Pass' = 0, 'Take On' = 0,'Foul' = 0,'Tackle' = 0,
                    'Interception' = 0,'Shot' = 0,'Challenge' = 0, 'Error' = 0)


for (i in 1:nrow(player)){
  id = player$player_id[i]
  feature = total(id)
  k.data[i,]<- c(player$player_id[i],player$position[i], feature)
}



total<- function(id){
 # select the player 
  ex = filter(info, player_id == id)
  ex = select(ex, game_id, type_id, outcome)
 # number of games 
  game.number<- length(unique(ex$game_id))
 # features
  feature<- c(1,3,4,7,8,13,14,15,16,45,51)
 # add something to avoid none in feature
  ex[c((nrow(ex) + 1): (nrow(ex) +length(feature))),]<- c(feature,feature,feature)
 # calculate total number of each event 
  ex<- ex%>%
         filter(type_id %in% feature)%>%
         group_by(type_id)%>%
         summarise(count = n())
  # put temp goal together
  temp<- sum(ex$count[6:9])
  #
  feature.count<- ex$count[-7:-9]
  feature.count[6]<- temp
  feature.count<- feature.count/game.number
  return(feature.count)
}

data1<- filter(k.data, Pass<=65 & Pass>=4)

kmeans.data<- data1[,c(3:10)]
kk<- kmeans(kmeans.data, 3)

compare<- data1[,c(1,2)]
compare$kmean<- kk$cluster
