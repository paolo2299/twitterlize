#!/bin/bash

echo "running locations..."
python stream_daemon.py locations &
sleep 10
echo "running entities1..."
python stream_daemon.py entities1 &
sleep 10
echo "running entities2..."
python stream_daemon.py entities2 &
sleep 10
echo "running entities3..."
python stream_daemon.py entities3 &
