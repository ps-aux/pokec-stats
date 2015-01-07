class GenderStats(object):
    
    def __init__(self, age, male_count, female_count):
        self.age =  age
        self.male_count = male_count
        self.female_count = female_count
        
class RegionStats(object):
    
    all_gender_stats = {}
    
    def __init__(self, region):
        self.region = region
    
    def add_gender_stats(self, gender_stats):
        key = gender_stats.age
        self.all_gender_stats[key] = gender_stats
    
        
def create_report(region_stats_list, min_age, max_age):
    
    delimiter = ","
    
    #First line
    row = ["Region ->"]
    for stat in region_stats_list:
        row.append(stat.region)
        row.append("") #Empty place as region label should take 2 columns
    
    #Collection of all rows (strings)
    rows = [delimiter.join(row)]    
        
    #Second line
    row = ["Age"]
    for stat in region_stats_list:
        row.append("M")
        row.append("F")

    rows.append(delimiter.join(row))
    
    for age in range(min_age, max_age + 1):
        row = [str(age)]
        for stat in region_stats_list:
            gender_stats = stat.all_gender_stats[age]
            male_count = str(gender_stats.male_count)
            female_count = str(gender_stats.female_count)
            row.append(male_count)
            row.append(female_count)

        rows.append(delimiter.join(row))

    return "\n".join(rows)

        
mn = 14 
mx = 63

s1 = RegionStats("BA")
for a in range(mn, mx + 1):
    s1.add_gender_stats(GenderStats(a, 111, 222))

s2 = RegionStats("KO")
for a in range(mn, mx + 1):
    s1.add_gender_stats(GenderStats(a, 333, 555))

stats = [s1, s2]

report = create_report(stats, mn, mx)
print report

f = open("/home/arkonix/tmp/scrap.csv","w")
print >>f, report


