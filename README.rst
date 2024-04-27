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


=========================
how to setup flask server
=========================

.. code-block:: text

	usage: parking_lot [-h] [--log_level LOG_LEVEL] [--daily_fee DAILY_FEE] [--hourly_fee HOURLY_FEE] {runserver} ...

	parging lot

	positional arguments:
	{runserver}           sub-command help
		runserver           run flask server

	options:
	-h, --help            show this help message and exit
	--log_level LOG_LEVEL
									nivel de log
	--daily_fee DAILY_FEE
									set the daily fee
	--hourly_fee HOURLY_FEE
									set the hourly fee

**********
run server
**********

.. code-block:: bash

	parking_lot runserver

to change the port

.. code-block:: bash

	parking_lot runserver -p 8080

change the fees


.. code-block:: bash

	parking_lot --daily_fee 10 --hourly_fee 2 runserver -p 8080


*****************
call the services
*****************

.. code-block:: bash

	curl  'http://127.0.0.1:8000/add?car=X774HY98&tariff=hourly'
	curl  'http://127.0.0.1:8000/remove?location=0'
	curl  'http://127.0.0.1:8000/list'

