===========
parking_lot
===========


small service for admin a parking lot


=======
install
=======


.. code-block:: bash

	git clone https://github.com/dem4ply/parking_lot.git
	pip install -e parking_lot


===========
how to used
===========


.. code-block:: python

	from parking_lot.parking_lot import Parking_lot
	# create parking lot with 10 spaces
	parking_lot = Parking_lot(amount=10)
	parking_lot.add(car='X774HY98', tariff='hourly')
	parking_lot.add(car='28A 8117', tariff='daily')
	parking_lot.add(car='667D', tariff='hourly')
	parking_lot.add(car='430-GOI', tariff='daily')

	car = parking_lot.remove( 2 )
	# print license plate, hourly tariff and fee
	print( car.car, car.tariff, car.fee )
	car = parking_lot.remove( 1 )
	# print license plate, daily tariff and fee
	print( car.car, car.tariff, car.fee )
