{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#import numpy as np\n",
    "#import pandas as pd\n",
    "import datetime as dt\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func, desc\n",
    "from flask import Flask, jsonify, request\n",
    "# from werkzeug.wrappers import Request, Response"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# sqlite setup\n",
    "engine = create_engine('sqlite:///Resources/hawaii.sqlite', echo=False)\n",
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "session = Session(engine)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Flask\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# landing page\n",
    "@app.route(\"/\")\n",
    "\n",
    "def Landing_Page():\n",
    "\n",
    "    return (\"<h1> Weather app Landing PagePage</h1><br>\"\n",
    "\n",
    "            f\"<h2>Append link from below to url to see page.</h2><br>\"\n",
    "\n",
    "            f\"<h3>/api/v1.0/stations</h3><br>\"\n",
    "            f\"<h3>/api/v1.0/precipitation</h3><br>\"\n",
    "\n",
    "            f\"<h3>/api/v1.0/tobs</h3><br>\"\n",
    "\n",
    "            f\"Add YYYY-MM-DD format day at the end of this url to retrieve the recorded min, avg, and max temps since a set date<br>\"\n",
    "\n",
    "            f\"<h3>/api/v1.0/</h3><br>\"\n",
    "\n",
    "            f\"Add YYYY-MM-DD format day at the end of this ur to retrieve the recorded min, avg, and max temps between two dates<br>\"\n",
    "\n",
    "            f\"<h3>/api/v1.0/</h3><br>\"\n",
    "\n",
    "             )\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Precipitation page\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "\n",
    "def precipitation():\n",
    "\n",
    "    session = Session(engine)\n",
    "    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()\n",
    "    datetime = datetime.strptime(date[0], \"%Y-%m-%d\")\n",
    "    last_year = datetime_obj - timedelta(days=365)\n",
    "    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > last_year).all()\n",
    "\n",
    "    DT = {}\n",
    "\n",
    "    for date, prcp in precip:\n",
    "\n",
    "        dates[date] = prcp\n",
    "\n",
    "    return jsonify(DT)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# stations page\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "\n",
    "def stations():\n",
    "\n",
    "    session = Session(engine)\n",
    "\n",
    "    stations = session.query(Station.station, Station.name).all()\n",
    "\n",
    "    stationlist = list(np.ravel(stations))\n",
    "\n",
    "    return jsonify(stationlist)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# tobs\n",
    "\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "\n",
    "def tobs():\n",
    "\n",
    "    session = Session(engine)\n",
    "\n",
    "    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()\n",
    "\n",
    "    datetime = datetime.strptime(date[0], \"%Y-%m-%d\")\n",
    "\n",
    "    yearAgo = datetime_obj - timedelta(days=365)\n",
    "\n",
    "    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > yearAgo).all()\n",
    "\n",
    "    tobslist = list(np.ravel(tobs))\n",
    "\n",
    "    return jsonify(tobslist)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# start date page\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "\n",
    "def start(start):\n",
    "\n",
    "    session = Session(engine)\n",
    "\n",
    "    startList = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()\n",
    "\n",
    "    return jsonify(startList)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# start and end date page\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "\n",
    "def startEnd(start, end):\n",
    "\n",
    "    session = Session(engine)\n",
    "\n",
    "    startEndList = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()\n",
    "\n",
    "    return jsonify(startEndList)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: Do not use the development server in a production environment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with stat\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "120",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 120\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\jcfis\\Anaconda3\\lib\\site-packages\\IPython\\core\\interactiveshell.py:2969: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.\n",
      "  warn(\"To exit: use 'exit', 'quit', or Ctrl-D.\", stacklevel=1)\n"
     ]
    }
   ],
   "source": [
    "\n",
    "if __name__ == \"__main__\":\n",
    "\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
