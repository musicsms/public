#!/usr/bin/env python

from boto3 import resource, client


def get_region_names():
    conn = client('ec2')
    res = conn.describe_regions()
    regions = []
    for r in res['Regions']:
        regions.append(r['RegionName'])
    return regions


def tags_for_region(region_name):
    tags = set()
    res = resource('ec2', region_name=region_name)
    count = 0
    for i in res.instances.all():
        count += 1
        if i.tags is None:
            continue
        for t in i.tags:
            tags.add(t['Key'])
    print('Examined %d instances in %s'% (count, region_name))
    return tags


def main():
    tags = set()
    regions = get_region_names()
    for r in regions:
        tags.update(tags_for_region(r))
    print('Found %d distinct tag names:' % len(tags))
    for t in sorted(tags):
        print(t)

if __name__ == "__main__":
    main()
