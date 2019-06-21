SELECT
idx,band,cat,yeart,pricenow,pricenew,regtime,
1-POWER(pricenow/pricenew,12/(594-regtime)) AS r  
FROM cars LIMIT 100


CREATE TABLE pricelr AS 
SELECT
idx,band,cat,yeart,pricenow,pricenew,regtime,
1-POWER(pricenow/pricenew,12/(594-regtime)) AS r  
FROM cars


SELECT band,r FROM pricelr
WHERE r>0.03
ORDER BY band

SELECT band,AVG(r) FROM pricelr
WHERE r>0.03
GROUP BY band 

SELECT 
idx ,band,cat,ROUND(r*1000) AS pr
FROM pricelr

CREATE TABLE prcount AS 
SELECT 
ROUND(r*1000) AS pr
FROM pricelr

SELECT pr,COUNT(pr) AS n
FROM prcount 
GROUP BY py 
ORDER BY pr DESC 

SELECT COUNT(pr)
FROM prcount
WHERE pr<50

CREATE TABLE cars(
	idx BIGINT AUTO_INCREMENT PRIMARY KEY,
	band VARCHAR(16),
	cat VARCHAR(32),
	yeart INT,
	pricenow FLOAT,
	pricenew FLOAT,
	regtime INT,
	wkms FLOAT,
	pb INT,
	lit FLOAT,
	turbo INT,
	hp INT,
	stru INT,
	cys INT,
	regs INT,
	ycdate INT,
	jqdate INT,
	sydate INT,
	gears INT,
	gt INT
);
INSERT INTO cats(band,cat,yeart,pricenow,pricenew,regtime,wkms,pd,lit,turbo,hp,stru,cys,regs,ycdate,jqdate,sydate,gears,gt)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)


SELECT POWER(27,1/3)

CREATE TABLE pricelr AS
SELECT idx,band,cat,pricenow,pricenew,regtime,
1 - POWER(pricenow/pricenew,12/(594-regtime)) AS r FROM cars;

SELECT band,r,pricenow,pricenew FROM pricelr  WHERE r>=0.03 ORDER BY band;

SELECT band,AVG(r) AS ar FROM pricelr WHERE r>0.03 GROUP BY band;

CREATE TABLE prcount AS
SELECT idx,band,cat,pricenow,pricenew,ROUND(r*1000) AS pr FROM pricelr;

SELECT band,cat,pr,COUNT(pr),pricenow,pricenew AS n 
FROM prcount
GROUP BY pr
ORDER BY pr DESC;


CREATE TABLE bandplr
SELECT  band,cat,AVG(r) AS ar
FROM pricelr WHERE r>0.05 GROUP BY band,cat;


# 换算
SELECT * FROM
cars a INNER JOIN bandplr b ON a.band=b.band AND a.cat=b.cat
ORDER BY pricenew-pricenow

SELECT a.*,b.r FROM 
cars a LEFT JOIN pricelr b
ON a.idx = b.idx

SELECT a.idx,b.r, a.pricenew,a.regtime,a.wkms,pd,lit,turbo,hp,stru,cys,regs,ycdate,jqdate,sydate,gears,gt FROM
cars a LEFT JOIN pricelr b
ON a.idx=b.idx
WHERE r>0.05;

CREATE TABLE dataset AS
SELECT a.idx,b.r AS `y`,c.ar AS px,
a.pricenew,a.regtime,a.wkms,pd,lit,turbo,hp,stru,cys,regs,ycdate,jqdate,sydate,gears,gt FROM
cars a LEFT JOIN pricelr b
ON a.idx=b.idx 
INNER JOIN bandplr AS c
ON a.band = c.band
AND a.cat = c.cat
WHERE b.r>0.05;