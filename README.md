# Table of Contents
1. [Implementation, Thought Process](README.md#Implementation,Process)
2. [Repo Directory Structure Dataset](README.md###Repo_Directory_Structure)
3. [Tests](README.md##Tests)


# Implementation,Process

Not being able to use Pandas, was definitely of bummer but of course it would all have been too easy.

I figured I would use a set to keep track of unique drug prescribers and a dicitionary to map drugs to aggregated cost and presciber count. 

First implementation: 
In pseudo-code, I used two dictionaries, one dicitonary map the drugs to a list 
[prescriber_count, total_cost] and another to map the drugs to prescriber names. This in theory would work
for a small data set but wouldn't scale nicely for a large data set (The dictionaries would become incredible large and sorting would be a pain).

I backtracked a little and realized that to scale I needed to process the data in chunks; instead of processing the data as a whole and keeping large dictionaries I would process a chunk at a time. However, simply chunking the unsorted data wasn't going to work. I needed to find a way to chunk data where each chunk had a relation and was sorted, I also knew that keeping the entries inside a dictionary would faciliate the process.

Instead of reading the data line by line, it was better to read it using the csv module into a dictionary using the csv.DictReader(). Essentially I created a data frame rame as you would in Pandas
but in a dictionary format where each entry has the fields as a key and entry value as the value. Now that I had access to every entry and it was processed in this 'data frame', I was able to sort the entries by drug_name. With the data sorted in drug_name I could now chunk the date by drug drug_name!!!
That meant that I could process data by groups associated with the drug_name and the data structures used would only contain data for this group and would reset for another group.

All of the data was already in a dictionary-type data frame facilitating sorting,grouping/chunking, and access. Sorting and grouping the data then faciliated the aggregation and the need for building large and additional data structures.

There are two model decisions I made.

First, the entries were processed as strings so I needed to cast/convert the price string to either an int or float. There are some casted values that we want to prevent, for example 'NaN' or '-infinity'. If we casted everything to a float we would have to have to make a check that the result is a valid number. An int() cast, however, throws an error for these cases rather can converting them. To account for this, a cost an entry is casted to a float only if there exists a decimal point in it. Note: if precision or significant digits matter when adding the floats, it would be based on our objective if round, get the floor, or limit the sig figs.

Second, when the casting of the entry raised an exception, I invalidated that entry meaning I didn't increment the aggregate cost nor the prescriber count (I treated this entry as a removed entry). This model decision would have varied depending on what the aggregate data is used for; there are many ways to take care of NULL values (removing rows with null values, replacing null values with mean/mode/median, finding relationships between values, trying to clean the entry if there is a small typo for example clean '110000"' to '110000"',and predicting the values) and each method has it's pros and cons. Removing the whole row simplifies the code and evades a lot of computational errors.

To invalidate this entry, I didn't increment the aggregate or UNIQUE prescriber count (essentially removing the whole row and not taking into account). My program returns aggregate data for rows with VALID values. If I incremented the prescriber count for an invalid cost entry I would result in an aggregate row that would not accurately reflect the total cost. And that is the tradeoff, that the relation between prescriber count and total cost remains accurate but the complete UNIQUE prescriber count isn't. 



## Repo_Directory_Structure:


    ├── README.md 
    ├── run.sh
    ├── src
    │   └── pharmacy-counting.py
    ├── input
    │   └── itcont.txt
    ├── output
    |   └── top_cost_drug.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── top_cost_drug.txt
            ├── your-own-test_1
            |    ├── input
            |    │   └── your-own-input-for-itcont.txt
            |    |── output
            |        └── top_cost_drug.txt
            ├── test_cost_enries
            |    ├── input
            |    │   └── itcont.txt
            |    |── output
            |    |   └── top_cost_drug.txt
            ├── test_prescriber_name
                 ├── input
                 │   └── itcont.txt
                 |── output
                     └── top_cost_drug.txt

## Tests 
* test_1: Test default functionality; if content is aggregated according to unique prescriber count and aggregate cost per drug.

* test_cost_entries: Test different and invalid entries (0, NaN, Null, None, entries with non-numerical characters.). Tests that order is updated when taking into account invalid cost entries and invalid cost entries reflect a non-update on the prescriber count. Additionally I tested an entry that fits nicely with our second model decision. Say there is only 1 row with a unique drug but that row has an invalid entry for the drug cost. Here it is not possible to replace with mean/mode/medium and to make a prediction you would have to look at similar drugs, which requires knowledge of those drugs. Instead, we completely disregard that entire row. [note: we can possible return that entry with a pre-defined entry to signal that a user is prescribed to that drug but we don't know the cost].
Test negative and infinity cost entries (both are treated as if cost = 0) 


* test_prescriber_name: Test that the aggregate prescribers of a drug are unique and despite the value of the first and/or last name entry, they are considered different prescribers ( exception: first and last name are blank or empty space which results in being 1 unique prescriber, we could have discarded the whole role but to keep uniformity in decision model, if the cost entry is valid we assume that at least 1 prescriber is tied to that cost and a result we have a representation for that drug rather than none. Space after or before first name is still the same prescriber (if we were using the id instead of prescriber last and first name to identify prescriber, we would simply check the id)


Note: I did not test drug names, rather a drug name is unique according to it's entry, empty or not.

## Used Libraries
* from itertools import groupby
* import csv
* import sys
* import math








