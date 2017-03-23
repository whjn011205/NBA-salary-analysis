--------- Active players list current season ------------

# get the active player list in 2014-15
CREATE TABLE temp_current_players AS 
	SELECT playerID FROM Game WHERE season = "2014-15" GROUP BY playerID;;

SELECT count(*) FROM temp_current_players;;
[output]:492


# 
Create table temp_average_statistic as 
select playerID, season, avg(age) as age, avg(weight) as weight, sum(salary) as salary, avg(2014-debut) as exp  from Game 
inner join Salary using (playerID,season)
inner join Player using (playerID)
where season="2014-15"
group by playerID, season

select avg(age), avg(weight),avg(salary), avg(exp) from temp_average_statistic 
[output]: 26.5599173553719,100.049586776859,5468773.81818182,4.71900826446281


# count how many players in each position.
CREATE TABLE temp_player_pos_1415 AS 
	SELECT playerID, pos, count(season) AS cnt FROM Game 
	WHERE season="2014-15" 
	GROUP BY playerID, pos;;
					

SELECT pos, count(playerID) AS count FROM temp_player_pos_1415 GROUP BY pos;;
[output]:
## Note: Some players played more than 1 positions in 2014-15, 
## thus sum of players of all positions are larger than total number of active players in 2014-15  
C,86
PF,110
PF-SF,1
PG,99
PG-SG,2
SF,92
SF-PF,1
SF-SG,1
SG,113
SG-PG,2
SG-SF,1
--------- Average Career Salary -------------

#calculate the career salary upto 2014-15
CREATE TABLE temp_career_salary_upto_1415 AS 
	SELECT playerID, sum(salary) AS career_salary FROM Salary
	WHERE season<="2014-15" GROUP BY playerID;;

SELECT avg(career_salary) FROM temp_career_salary_upto_1415 
INNER JOIN temp_current_players USING (playerID);; 
[Output]: 27010234.2028689

-------- Average Experience -------------
CREATE TABLE temp_player_seasons AS 
	SELECT playerID, season FROM Game 
	WHERE season<="2014-15" GROUP BY playerID, season;;

CREATE TABLE temp_experience_upto_1415 AS 
	SELECT playerID, count(season) AS experience FROM temp_player_seasons 
	GROUP BY playerID;;

SELECT avg(experience) FROM temp_experience_upto_1415 INNER JOIN temp_current_players USING (playerID);;
[output]: 5.66056910569106

------- Average Salary in 2014-15 ----------------------
SELECT avg(salary) FROM Salary INNER JOIN temp_current_players USING (PlayerID) WHERE season="2014-15";;
[output]:4059140.40618956


## CREATE TABLE temp_salary_1415 AS SELECT playerID, sum(salary) AS salary FROM Salary WHERE season ="2014-15" GROUP BY playerID;;

## Top 10% paid
SELECT playerID, salary, teamName, Player.fullname FROM Salary 
JOIN Player USING(PlayerID) 
WHERE season="2014-15" and salary !=""
ORDER BY salary DESC 
LIMIT (SELECT count(playerID) FROM temp_salary_1415)/10-1 ;;

## Bottom 10% paid
SELECT playerID, salary, teamName, Player.fullname FROM Salary 
JOIN Player USING(PlayerID) 
WHERE season="2014-15" and salary !=""
ORDER BY salary ASC 
LIMIT (SELECT count(playerID) FROM temp_salary_1415)/10-1 ;;

## Middle 50% paid
SELECT playerID, salary, teamName, Player.fullname FROM Salary 
JOIN Player USING(PlayerID) 
WHERE season="2014-15" and salary !=""
ORDER BY salary DESC 
LIMIT (SELECT count(playerID) FROM temp_salary_1415)/2-1
OFFSET (SELECT count(playerID) FROM temp_salary_1415)/4;;

--------------Total paid by season-------------------
CREATE TABLE temp_active_players_salary AS 
	SELECT playerID, season,  sum(Salary.salary) as salary FROM Game 
	JOIN Salary USING(PlayerID,season,teamName) 
	INNER JOIN temp_current_players USING(PlayerID)
	where season<="2014-15"
	group by playerID, season

CREATE TABLE temp_active_players_total_salary AS
	SELECT season, sum(salary) AS total, count(salary) AS count
	FROM temp_active_players_salary 
	GROUP BY season

SELECT season, total/count FROM temp_active_players_total_salary
GROUP BY season

------------------------------
CREATE TABLE temp_playersalary_season AS
	SELECT playerID, season, teamName, sum(salary) AS player_salary  FROM Salary 
	WHERE season<="2014-15"
	GROUP BY playerID, season, teamName


CREATE TABLE temp_avgsalary_season AS
	SELECT season, teamName, avg(player_salary) AS mean, count(player_salary) AS count FROM temp_playersalary_season
	WHERE season<="2014-15"
	GROUP BY season, teamName
	
CREATE TABLE temp_playersalary_variance_season AS
	SELECT teamName, season, SUM((player_salary-mean)*(player_salary-mean))/count AS variance
	FROM temp_playersalary_season
	INNER JOIN temp_avgsalary_season USING (season,teamName)
	GROUP BY teamName,season
---------------------- pivot teamsalary---------------------------

create table temp_pivot_team_avgsalary as 
SELECT teamName,  
sum(CASE WHEN season="1985-86" THEN mean END) AS s1985_86,
sum(CASE WHEN season="1987-88" THEN mean END) AS s1987_88,
sum(CASE WHEN season="1988-89" THEN mean END) AS s1988_89,
sum(CASE WHEN season="1990-91" THEN mean END) AS s1990_91,
sum(CASE WHEN season="1991-92" THEN mean END) AS s1991_92,
sum(CASE WHEN season="1992-93" THEN mean END) AS s1992_93,
sum(CASE WHEN season="1993-94" THEN mean END) AS s1993_94,
sum(CASE WHEN season="1994-95" THEN mean END) AS s1994_95,
sum(CASE WHEN season="1995-96" THEN mean END) AS s1995_96,
sum(CASE WHEN season="1996-97" THEN mean END) AS s1996_97,
sum(CASE WHEN season="1997-98" THEN mean END) AS s1997_98,
sum(CASE WHEN season="1998-99" THEN mean END) AS s1998_99,
sum(CASE WHEN season="1999-00" THEN mean END) AS s1999_00,
sum(CASE WHEN season="2000-01" THEN mean END) AS s2000_01,
sum(CASE WHEN season="2001-02" THEN mean END) AS s2001_02,
sum(CASE WHEN season="2002-03" THEN mean END) AS s2002_03,
sum(CASE WHEN season="2003-04" THEN mean END) AS s2003_04,
sum(CASE WHEN season="2004-05" THEN mean END) AS s2004_05,
sum(CASE WHEN season="2005-06" THEN mean END) AS s2005_06,
sum(CASE WHEN season="2006-07" THEN mean END) AS s2006_07,
sum(CASE WHEN season="2007-08" THEN mean END) AS s2007_08,
sum(CASE WHEN season="2008-09" THEN mean END) AS s2008_09,
sum(CASE WHEN season="2009-10" THEN mean END) AS s2009_10,
sum(CASE WHEN season="2010-11" THEN mean END) AS s2010_11,
sum(CASE WHEN season="2011-12" THEN mean END) AS s2011_12,
sum(CASE WHEN season="2012-13" THEN mean END) AS s2012_13,
sum(CASE WHEN season="2013-14" THEN mean END) AS s2013_14,
sum(CASE WHEN season="2014-15" THEN mean END) AS s2014_15

from temp_avgsalary_season
group by teamName
order by teamName;

------------------age-----------------
CREATE TABLE temp_age_nodup AS
	SELECT playerID, season, teamName, avg(age) AS age FROM Game
	WHERE season<="2014-15"
	GROUP BY playerID, season,teamName

CREATE TABLE temp_avgage_team_season AS
	SELECT teamName,season, avg(age) AS avg_age, count(age) as count FROM temp_age_nodup
	GROUP BY teamName, season

CREATE TABLE temp_avgage_variance_team_season AS
	SELECT teamName, season, SUM((age-avg_age)*(age-avg_age))/count AS variance FROM temp_age_nodup
	INNER JOIN temp_avgage_team_season USING ( teamName, season)
	GROUP BY teamName, season
	
CREATE TABLE temp_pivot_team_avgage AS 
SELECT teamName,  
sum(CASE WHEN season="1985-86" THEN avg_age END) AS s1985_86,
sum(CASE WHEN season="1987-88" THEN avg_age END) AS s1987_88,
sum(CASE WHEN season="1988-89" THEN avg_age END) AS s1988_89,
sum(CASE WHEN season="1990-91" THEN avg_age END) AS s1990_91,
sum(CASE WHEN season="1991-92" THEN avg_age END) AS s1991_92,
sum(CASE WHEN season="1992-93" THEN avg_age END) AS s1992_93,
sum(CASE WHEN season="1993-94" THEN avg_age END) AS s1993_94,
sum(CASE WHEN season="1994-95" THEN avg_age END) AS s1994_95,
sum(CASE WHEN season="1995-96" THEN avg_age END) AS s1995_96,
sum(CASE WHEN season="1996-97" THEN avg_age END) AS s1996_97,
sum(CASE WHEN season="1997-98" THEN avg_age END) AS s1997_98,
sum(CASE WHEN season="1998-99" THEN avg_age END) AS s1998_99,
sum(CASE WHEN season="1999-00" THEN avg_age END) AS s1999_00,
sum(CASE WHEN season="2000-01" THEN avg_age END) AS s2000_01,
sum(CASE WHEN season="2001-02" THEN avg_age END) AS s2001_02,
sum(CASE WHEN season="2002-03" THEN avg_age END) AS s2002_03,
sum(CASE WHEN season="2003-04" THEN avg_age END) AS s2003_04,
sum(CASE WHEN season="2004-05" THEN avg_age END) AS s2004_05,
sum(CASE WHEN season="2005-06" THEN avg_age END) AS s2005_06,
sum(CASE WHEN season="2006-07" THEN avg_age END) AS s2006_07,
sum(CASE WHEN season="2007-08" THEN avg_age END) AS s2007_08,
sum(CASE WHEN season="2008-09" THEN avg_age END) AS s2008_09,
sum(CASE WHEN season="2009-10" THEN avg_age END) AS s2009_10,
sum(CASE WHEN season="2010-11" THEN avg_age END) AS s2010_11,
sum(CASE WHEN season="2011-12" THEN avg_age END) AS s2011_12,
sum(CASE WHEN season="2012-13" THEN avg_age END) AS s2012_13,
sum(CASE WHEN season="2013-14" THEN avg_age END) AS s2013_14,
sum(CASE WHEN season="2014-15" THEN avg_age END) AS s2014_15

from temp_avgage_team_season
group by teamName
order by teamName;

	