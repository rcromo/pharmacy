from itertools import groupby
import csv
import sys
import math


def aggregate_entries(filename):
	"""
	Aggregates the entries of a csv file to determine the total cost and UNIQUE count
	per drug.

    param filename: name of the csv file
    return: list of aggregated entries in dictionary format
    """
	agg_entries = list()
	with open(filename, 'r') as file:
		
		# reads the file into a dictionary format where column name is the key, entry value is the value
		reader = csv.DictReader(file)
		# sorts and then groups the entries by drug_name
		sorted_reader = sorted(reader, key= lambda x: x['drug_name'])
		# groupby returns an interator: key, group
		groups = groupby(sorted_reader, key = lambda x: x['drug_name'])

		for drug_name, drug_group in groups:

			total_cost = 0
			num_prescriber = total_cost = 0
			prescribers = set()

			for entry in drug_group:
				
				try:
					curr_cost = entry["drug_cost"]
					if '.' in curr_cost:
						cost = float(curr_cost)
					else:
						cost = int(curr_cost)
				# detect conversion erros and null values
				except (ValueError, TypeError) as err:
					#signifies invalid entry
					cost = -1
			
				# strip spaces before and after first name to keep uniqueness in prescriber name
				prescriber = entry['prescriber_last_name'].strip() + ',' + entry['prescriber_first_name'].strip()
				# discard null entries by not incrementing cost and prescriber_count
				if (prescriber not in prescribers) and (cost >= 0):
   					prescribers.add(prescriber)
   					num_prescriber = num_prescriber + 1
   					total_cost = total_cost + cost

			if total_cost != 0:
				# format entries to facilate dumping of aggregate content
				agg_entries.append(
					{"drug_name": drug_name,
			         "num_prescriber": num_prescriber,
			         "total_cost": total_cost})

	return agg_entries

def main():
	"""Takes in a prescription drugs file, aggregates the data by cost and unique prescriber
	count per drug, and outputs to a .txt file.
    """
	INPUT_PATH = sys.argv[1]
	OUTPUT_PATH = sys.argv[2]

	entries = aggregate_entries(INPUT_PATH)

	with open(OUTPUT_PATH, 'w') as file:
		fieldnames = ["drug_name", "num_prescriber", "total_cost"]
		writer = csv.DictWriter(file, fieldnames= fieldnames)
		writer.writeheader()
		# have sorted groups by drug_name, not sort by total_cost
		for entry in sorted(entries, key = lambda x: x['total_cost'], reverse = True):
			writer.writerow(entry)



if __name__ == "__main__":
	main()