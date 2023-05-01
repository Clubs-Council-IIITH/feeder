#!/usr/bin/env bash
# config
DATA_DIR=/data

did_nothing=1 # check if the script did anything at all
timestamp=$(date "+%F_%T") # track timestamp for renaming uniformity

# push clubs
if [[ -f "$DATA_DIR/clubs.csv" ]]
then
    echo "Pushing clubs..."

    # rename file once done
    mv $DATA_DIR/clubs.csv $DATA_DIR/clubs_$timestamp.csv
    did_nothing=0
fi

# push events
if [[ -f "$DATA_DIR/events.csv" ]]
then
    echo "Pushing events..."
    ./push_events.py $DATA_DIR/events.csv

    # rename file once done
    mv $DATA_DIR/events.csv $DATA_DIR/events_$timestamp.csv
    did_nothing=0
fi

# push members
if [[ -f "$DATA_DIR/members.csv" ]]
then
    echo "Pushing members..."

    # rename file once done
    mv $DATA_DIR/members.csv $DATA_DIR/members_$timestamp.csv
    did_nothing=0
fi

# push users
if [[ -f "$DATA_DIR/users.csv" ]]
then
    echo "Pushing users..."

    # rename file once done
    mv $DATA_DIR/users.csv $DATA_DIR/users_$timestamp.csv
    did_nothing=0
fi

if [[ $did_nothing -eq 1 ]]
then
    echo "Nothing to do."
else
    echo "Done with everything."
fi
