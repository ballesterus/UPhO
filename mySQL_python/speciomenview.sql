SELECT idSpecimen,
GH_Number,
concat_ws(' ', Genus, Species ) AS Species_name,
femaleCount + maleCount + subAdultMaleCount + subAdultFemaleCount + juvenilesCount AS Amount,
concat_ws(': ',Country, State ) AS Geography,
LocalityName,
DecimalLong,
DecimalLat
FROM Specimen INNER JOIN Determination ON (Specimen.idDetermination = Determination.idDetermination)
INNER JOIN Species ON (Determination.idSpecies = Species.idSpecies)
INNER JOIN CollectionEvent ON (Specimen.idCollectionEvent = CollectionEvent.idCollectionEvent)
INNER JOIN Locality ON (CollectionEvent.idLocality = Locality.idLocality);