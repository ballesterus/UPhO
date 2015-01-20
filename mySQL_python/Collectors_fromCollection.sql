SELECT 
    CollectionEvent.idCollectionEvent AS IdNum,
    CollectionDate,
	Country,
	LocalityName,
	group_concat(LastName SEPARATOR ', ') AS Collected_by
FROM
    CollectionEvent
        INNER JOIN
    Locality ON (CollectionEvent.idLocality = Locality.idLocality)
        INNER JOIN
    Collectors ON (Collectors.idCollectionEvent = CollectionEvent.idCollectionEvent)
        INNER JOIN
    Personel ON (Collectors.idPersonel = Personel.idPersonel)
GROUP BY idNum
	;
	