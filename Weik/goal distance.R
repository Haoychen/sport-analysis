library(dplyr)

team<- read.csv('team.csv')
team.name<-  team$team_name[order(team$team_id)]
# goal position for 1230
la<- event %>%
       filter(type_id == 16 & team_id == 1230 & x < 45)%>%
       select(x, y)
       


# total goal for first half field. y = 0 means right
goal.first<- event %>%
                    filter(type_id == 16 & x > 45)%>%
                    group_by(team_id)%>%
                    summarise('x_distance' = sum(100 - x), 'y_distance' = sum(y), 'goal' = n())

# total goal for second half field
goal.second<- event %>%
                    filter(type_id == 16 & x < 45)%>%
                    group_by(team_id)%>%
                    summarise('x_distance' =sum(x),'y_distance' = sum(100 - y),'goal' = n())
#here is no information about team 1899. we add it manually
goal.second[c(15:19),]<- goal.second[c(14:18),]
goal.second[14,]<- c(1899, 0, 0, 0)

# calculate the number of games for each team
total.game <- event%>%
                   group_by(team_id)%>%
                   summarise('game' = n_distinct(game_id))

team.number <- length(total.game$team_id)

final <- data.frame(team_id = total.game$team_id, 'team_name' = team.name, 'x_distance' = c(1:team.number), 
                    y_distance = c(1:team.number), goal = c(1:team.number))

final$x_distance <- (goal.first$x_distance + goal.second$x_distance)/total.game$game
final$y_distance <- (goal.first$y_distance + goal.second$y_distance)/total.game$game
final$goal <- (goal.first$goal + goal.second$goal)/total.game$game

write.csv(final, 'goal_each_team.csv')
#draw
library(ggplot2)
ggplot(data = final,aes(x = x_distance, y = y_distance, labels = as.character(team.name))) + geom_point()




