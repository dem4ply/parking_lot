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
	parking_lot = Parking_lot( amount=10 )
	car = parking_lot.add( car='X774HY98', tariff='hourly' )
	car = parking_lot.remove( car.location )
	# print parking fee
	print( car.fee )
	car = parking_lot.add( car='X774HY98', tariff='daily' )
	car = parking_lot.remove( car.location )
	# print parking fee
	print( car.fee )
