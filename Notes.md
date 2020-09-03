## Download Offers

### AWS Documentation

https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-ppslong.html

### On Demand Pricing
https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.json
https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.csv

### Savings Plan

Get the current region index:
https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/current/region_index.json

Get the prices:
https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20200709193359/ap-southeast-2/index.csv

### 

## Fields

Instance Type
    - t3.micro

TermType:
 - OnDemand
 - Reserved

Tenancy:
    - Shared
    - Dedicated

Operating System:
    - Linux
    - RHEL
    - SUSE
    - Windows

License Model:
    - Bring your own license
    - No License required

usageType:
    - APS2-BoxUsage:t3.micro
    - APS2-DedicatedRes:t3.micro
    - APS2-DedicatedUsage:t3.micro
    - APS2-UnusedBox:t3.micro
    - APS2-UnusedDed:t3.micro
    - APS2-Reservation:t3.micro

CapacityStatus:
    - Used
    - AllocatedCapacityReservation
    - UnusedCapacityReservation

Pre Installed S/W:
    - NA
    - SQL Web

```
# field_of_interest = "TermType"  # OnDemand, Reserved
# field_of_interest = "Tenancy"  # Host, Reserved, Shared, Dedicated, NA
# field_of_interest = "Operating System"
# field_of_interest = "License Model"  # No License required, NA, Bring your own license
# field_of_interest = "CapacityStatus"  # UnusedCapacityReservation, AllocatedCapacityReservation, NA, Used, AllocatedHost
# field_of_interest = "Pre Installed S/W"
# field_of_interest = "Unit"
field_of_interest = "Currency"  # USD
# field_of_interest = ""  # Set to empty string to get available Headers
```

## Unique Key - 1
TermType: OnDemand
Tenancy: Shared
Operating System: Linux
License Model: No License required
CapacityStatus: Used
Pre Installed S/W: NA

## Unique Key - 2
TermType: OnDemand
Tenancy: Shared
Operating System: Linux
License Model: No License required
usageType: APS2-BoxUsage:t3.micro
Pre Installed S/W: NA
