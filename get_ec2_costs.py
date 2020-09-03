import requests
import argparse
import os
import yaml
import csv
from collections import OrderedDict
cache_dir = ".cache"


def download_aws_pricing_files(aws_region="ap-southeast-2"):
    aws_pricing_api_domain = "pricing.us-east-1.amazonaws.com"
    aws_pricing_ec2_current_region_index = "/offers/v1.0/aws/AmazonEC2/current/region_index.json"
    aws_pricing_ec2_savings_plan_current_region_index = \
        "/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/current/region_index.json"

    aws_pricing_ec2_filepath = ""
    aws_pricing_ec2_savings_plan_filepath = ""

    def get_url(path, domain=aws_pricing_api_domain):
        return "https://{}{}".format(domain, path)

    r = requests.get(get_url(aws_pricing_ec2_current_region_index))
    if r.status_code == 200:
        aws_pricing_ec2_current_index = r.json()["regions"][aws_region]["currentVersionUrl"]
        aws_pricing_ec2_current_index = aws_pricing_ec2_current_index[:-4] + "csv"
        aws_pricing_ec2_filepath = os.path.join(
            cache_dir, "AmazonEC2_{}_{}.csv".format(aws_region, aws_pricing_ec2_current_index.split('/')[5]))
        if not os.path.isfile(aws_pricing_ec2_filepath):
            print('Downloading "{}" from {}'.format(aws_pricing_ec2_filepath, get_url(aws_pricing_ec2_current_index)))
            download_file(get_url(aws_pricing_ec2_current_index), aws_pricing_ec2_filepath)

    r = requests.get(get_url(aws_pricing_ec2_savings_plan_current_region_index))
    if r.status_code == 200:
        for region_data in r.json()["regions"]:
            if region_data["regionCode"] == aws_region:
                aws_pricing_ec2_savings_plan_current_index = region_data["versionUrl"]
                break
        aws_pricing_ec2_savings_plan_current_index = aws_pricing_ec2_savings_plan_current_index[:-4] + "csv"
        aws_pricing_ec2_savings_plan_filepath = os.path.join(cache_dir, "AmazonEC2_SavingsPlan_{}_{}.csv".format(
            aws_region, aws_pricing_ec2_savings_plan_current_index.split('/')[5]))
        if not os.path.isfile(aws_pricing_ec2_savings_plan_filepath):
            print('Downloading "{}" from {}'.format(aws_pricing_ec2_savings_plan_filepath,
                                                    get_url(aws_pricing_ec2_savings_plan_current_index)))
            download_file(get_url(aws_pricing_ec2_savings_plan_current_index), aws_pricing_ec2_savings_plan_filepath)
    return aws_pricing_ec2_filepath, aws_pricing_ec2_savings_plan_filepath


def download_file(url, filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return filename


def trim_aws_pricing_files(aws_pricing_ec2_filepath, aws_pricing_ec2_savings_plan_filepath):
    trimmed_aws_pricing_ec2_filepath = aws_pricing_ec2_filepath[:-3] + "_t.csv"
    trimmed_aws_pricing_ec2_savings_plan_filepath = aws_pricing_ec2_savings_plan_filepath[:-3] + "_t.csv"
    if not os.path.isfile(trimmed_aws_pricing_ec2_filepath):
        with open(aws_pricing_ec2_filepath, mode='r') as f:
            with open(trimmed_aws_pricing_ec2_filepath, mode='w') as t:
                t.writelines(f.readlines()[5:])
    if not os.path.isfile(trimmed_aws_pricing_ec2_savings_plan_filepath):
        with open(aws_pricing_ec2_savings_plan_filepath, mode='r') as f:
            with open(trimmed_aws_pricing_ec2_savings_plan_filepath, mode='w') as t:
                t.writelines(f.readlines()[5:])
    return trimmed_aws_pricing_ec2_filepath, trimmed_aws_pricing_ec2_savings_plan_filepath


def get_headers(ec2_pricing_csv_filepath):
    with open(ec2_pricing_csv_filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        headers = csv_reader.fieldnames
        for i, header in enumerate(headers):
            headers[i] = header.strip('"')
            print(headers[i])
    return headers


def get_header_options(ec2_pricing_csv_filepath, header):
    header_options = []
    with open(ec2_pricing_csv_filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for line in csv_reader:
            if line_count == 0:
                pass
            else:
                header_options.append(line[header])
            line_count += 1

        header_options = sorted(set(header_options))

        for header_option in header_options:
            print(header_option)
    return header_options


def get_default_config():
    config = {
        "headers": [
            # "SKU",
            "Instance Type", "TermType", "Tenancy", "Operating System", "License Model", "CapacityStatus",
           "Pre Installed S/W", "Unit", "PricePerUnit", "Currency"
        ],
        "savings_plan_headers": [
            "Compute AllUpfront 1Yr",
            "Compute AllUpfront 3Yr",
            "Compute PartialUpfront 1Yr",
            "Compute PartialUpfront 3Yr",
            "Compute NoUpfront 1Yr",
            "Compute NoUpfront 3Yr",
            "EC2 AllUpfront 1Yr",
            "EC2 AllUpfront 3Yr",
            "EC2 PartialUpfront 1Yr",
            "EC2 PartialUpfront 3Yr",
            "EC2 NoUpfront 1Yr",
            "EC2 NoUpfront 3Yr",
        ],
        "selection_criteria": {
            "Instance Type": [
                # "t2.micro", "t2.small", "t2.medium", "t2.large",
                # "t3.micro", "t3.small", "t3.medium", "t3.large", "t3.xlarge", "t3.2xlarge",
                # "t3a.large",
                # "m4.large", "m4.xlarge", "m4.2xlarge",
                # "r4.xlarge",
                # "r5.large", "r5.xlarge",
                # "m5.large", "m5.xlarge", "m5.2xlarge", "r5.24xlarge",  "r5.12xlarge",
                # "c5.xlarge"

            #     custom
                "r5.large", "m5.large", "t3.medium", "m5.large", "m4.xlarge"
            ],
            "TermType": ["OnDemand"],
            "Tenancy": ["Shared"],
            "Operating System": ["Linux", "Windows"],
            "License Model": ["No License required"],
            "CapacityStatus": ["Used"],
            "Pre Installed S/W": ["NA"],
        }
    }
    return config


def get_ec2s_meeting_selection_criteria(config, ec2_pricing_csv_filepath):
    def is_meeting_selection_criteria(selection_criteria, csv_line):
        meets_selection_criteria = False
        for key in selection_criteria.keys():
            for value in selection_criteria[key]:
                if csv_line[key] == value:
                    meets_selection_criteria = True
                    break
                else:
                    meets_selection_criteria = False
            if not meets_selection_criteria:
                break
        return meets_selection_criteria

    ec2s = []

    with open(ec2_pricing_csv_filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for csv_line in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if is_meeting_selection_criteria(config["selection_criteria"], csv_line):
                    # ec2_prices.append(extract_values_from_headers(csv_line, config["headers"]))
                    ec2s.append(csv_line)
                line_count += 1
    return ec2s


def get_savings_plan_prices_for_ec2s(list_of_ec2s, ec2_savings_plan_pricing_csv_filepath):
    def get_unique_skus_from_ec2s(list_of_ec2s):
        skus = []
        for ec2 in list_of_ec2s:
            if ec2["SKU"] in skus:
                print("Found non-unique SKU for:")
                print(ec2)
                exit(1)
            else:
                skus.append(ec2["SKU"])
        return skus

    def classify_savings_plan_price_key_and_value(savings_plan_line):
        if savings_plan_line["PurchaseOption"] == "All Upfront":
            spp_key_po = "AllUpfront"
        elif savings_plan_line["PurchaseOption"] == "Partial Upfront":
            spp_key_po = "PartialUpfront"
        elif savings_plan_line["PurchaseOption"] == "No Upfront":
            spp_key_po = "NoUpfront"
        else:
            print('Unrecognised "PurchaseOption": {}'.format(savings_plan_line["PurchaseOption"]))
            exit(1)

        if savings_plan_line["LeaseContractLength"] == '1':
            spp_key_lcl = "1Yr"
        elif savings_plan_line["LeaseContractLength"] == '3':
            spp_key_lcl = "3Yr"
        else:
            print('Unrecognised "LeaseContractLength": {}'.format(savings_plan_line["LeaseContractLength"]))
            exit(1)

        if savings_plan_line["Product Family"] == "ComputeSavingsPlans":
            spp_key_pf = "Compute"
        elif savings_plan_line["Product Family"] == "EC2InstanceSavingsPlans":
            spp_key_pf = "EC2"
        else:
            print('Unrecognised "Product Family"": {}'.format(savings_plan_line["Product Family"]))
            exit(1)

        savings_plan_price_key = " ".join([spp_key_pf, spp_key_po, spp_key_lcl])
        savings_plan_price_value = savings_plan_line["DiscountedRate"]

        return savings_plan_price_key, savings_plan_price_value

    def initialise_savings_plan_sku_lookup_map(skus):
        savings_plan_sku_lookup_map = {}
        for sku in skus:
            savings_plan_sku_lookup_map.update({sku: {
                "Compute AllUpfront 1Yr": "",
                "Compute AllUpfront 3Yr": "",
                "Compute PartialUpfront 1Yr": "",
                "Compute PartialUpfront 3Yr": "",
                "Compute NoUpfront 1Yr": "",
                "Compute NoUpfront 3Yr": "",
                "EC2 AllUpfront 1Yr": "",
                "EC2 AllUpfront 3Yr": "",
                "EC2 PartialUpfront 1Yr": "",
                "EC2 PartialUpfront 3Yr": "",
                "EC2 NoUpfront 1Yr": "",
                "EC2 NoUpfront 3Yr": "",
            }})
        return savings_plan_sku_lookup_map

    skus_to_find = get_unique_skus_from_ec2s(list_of_ec2s)
    savings_plan_sku_lookup_map = initialise_savings_plan_sku_lookup_map(skus_to_find)

    with open(ec2_savings_plan_pricing_csv_filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for line in csv_reader:
            if line_count == 0:
                pass
            elif line["DiscountedSKU"] in skus_to_find:
                savings_plan_price_key, savings_plan_price_value = classify_savings_plan_price_key_and_value(line)
                savings_plan_sku_lookup_map[line["DiscountedSKU"]][savings_plan_price_key] = savings_plan_price_value
            line_count += 1

    return savings_plan_sku_lookup_map


def get_ec2_pricing(config, ec2_pricing_csv_filepath, ec2_savings_plan_pricing_csv_filepath):
    def extract_values_from_headers(ec2_properties, headers):
        line = []
        for header in headers:
            line.append(ec2_properties[header])
        return line

    def get_ec2_savings_plan_prices(ec2, savings_plan_prices_map, savings_plan_headers):
        ec2_savings_plan_prices = []
        for savings_plan_header in savings_plan_headers:
            ec2_savings_plan_prices.append(savings_plan_prices_map[ec2['SKU']][savings_plan_header])
        return ec2_savings_plan_prices


    distilled_ec2s_list = []
    ec2s = get_ec2s_meeting_selection_criteria(config, ec2_pricing_csv_filepath)

    savings_plan_prices_map = get_savings_plan_prices_for_ec2s(ec2s, ec2_savings_plan_pricing_csv_filepath)


    for ec2 in ec2s:
        distilled_ec2s_list.append(
            extract_values_from_headers(ec2, config["headers"]) +
            get_ec2_savings_plan_prices(ec2, savings_plan_prices_map, config["savings_plan_headers"])
        )
    return distilled_ec2s_list


def write_ec2_prices_to_csv(ec2_prices, config, csv_filename="output.csv", delimiter=","):
    with open(csv_filename, 'w') as out_file:
        csv_out = csv.writer(out_file, delimiter=delimiter)
        csv_out.writerow(config["headers"] + config["savings_plan_headers"])
        for ec2_price in ec2_prices:
            csv_out.writerow(ec2_price)
    return


def main(command):
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)

    aws_pricing_ec2_filepath, aws_pricing_ec2_savings_plan_filepath = download_aws_pricing_files()
    ec2_file, ec2_sp_file = trim_aws_pricing_files(aws_pricing_ec2_filepath, aws_pricing_ec2_savings_plan_filepath)

    if command.get_headers:
        get_headers(ec2_file)
    elif command.get_header_options:
        get_header_options(ec2_file, command.get_header_options)
    elif command.get_default_config:
        get_default_config()
        print(yaml.dump(get_default_config()))
    else:
        # TODO
        config = get_default_config()
        ec2_prices = get_ec2_pricing(config, ec2_file, ec2_sp_file)
        write_ec2_prices_to_csv(ec2_prices, config)
        # for ec2_price in ec2_prices:
        #     print(ec2_price)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gets EC2 prices.')
    parser.add_argument('--get-headers', action="store_true",
                        help='a command', default=False)
    parser.add_argument('--get-header-options', action="store", metavar="HEADER",
                        help="a command", default=False)
    parser.add_argument('--get-default-config', action="store_true",
                        help='a command', default=False)
    args = parser.parse_args()
    # download_aws_pricing_files()
    main(args)
   #TODO get prices against appended against list of EC2 instances