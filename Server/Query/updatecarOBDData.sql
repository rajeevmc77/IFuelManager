insert into `obdService_carobddata` (id,VIN,RPM,Speed, created_at, FuelTankLevel)
SELECT id,VIN,RPM,Speed,created_at, 0 FROM `obdService_carjsonobddata`;
