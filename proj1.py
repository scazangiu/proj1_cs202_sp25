import sys
import unittest
import math
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)

#Task 1: 
@dataclass(frozen = True)
class GlobeRect:        #Represents a rectangular region of the globe
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float
    
@dataclass(frozen = True)
class Region:       #Describes the identity and terrain of a region.
    rect: GlobeRect
    name: str
    terrain: str #terrain must be one of "ocean", "mountains", "forest", "other"
    
@dataclass(frozen = True)    
class RegionCondition:      #Describes the current state of a region in a specific year.
    region: Region
    year: int
    pop: int
    ghg_rate: float
    
#Task 2
region_conditions = [RegionCondition(Region(
                        GlobeRect(35.5, 35.9, 139.5, 140.0), 
                        "Tokyo", "other"), 
                        2020, 37_000_000, 70_000_000.0),
                    RegionCondition(Region(
                        GlobeRect(40.5, 41.0, -74.3, -73.6), 
                        "New York City", "other"), 
                        2018, 20_000_000, 50_000_000.0),
                    RegionCondition(Region(
                        GlobeRect(-10.0, 10.0, -140.0, -120.0), 
                        "Central Pacific Patch", "ocean"), 
                        2015, 0, 1_000_000.0),
                    RegionCondition(Region(
                        GlobeRect(35.15, 35.45, -120.85, -120.55), 
                        "San Luis Obispo Hills", "mountains"), 
                        2022, 280_000, 2_000_000.0)]
                       
#Task 3
def emissions_per_capita(rc: RegionCondition) -> float:
    #Takes a RegionCondition and returns the tons of CO₂-equivalent per person in region per year.
    if rc.pop == 0:
        return 0.0
        
    return rc.ghg_rate / rc.pop

def area(gr: GlobeRect) -> float:
    #Takes a GlobeRect and returns the estimated surface area of the region in square kilometers.
    R = 6378.1
    λ1 = math.radians(gr.west_long)
    λ2 = math.radians(gr.east_long)
    φ1 = math.radians(gr.lo_lat)
    φ2 = math.radians(gr.hi_lat)
    
    change_in_lambda = λ2 - λ1
    if change_in_lambda < 0:
        change_in_lambda += 2 * math.pi
        
    A = R**2 * abs(change_in_lambda) * abs(math.sin(φ2) - math.sin(φ1))
    
    return A
    
def emissions_per_square_km(rc: RegionCondition) -> float:
    #Takes a RegionCondition and returns the tons of CO₂-equivalent per square kilometer.
    A = area(rc.region.rect)
    if A == 0:
        return 0.0
    return rc.ghg_rate / A
    

def densest(rc_list: list[RegionCondition]) -> str:
    #Takes a list of RegionCondition values and returns the name of the region with the highest population density
    def densest_helper(rc_list):
        if len(rc_list) == 1:
            return rc_list[0]

        first = rc_list[0]
        best = densest_helper(rc_list[1:])

        density_first = first.pop / area(first.region.rect)
        density_best = best.pop / area(best.region.rect)

        if density_first > density_best:
            return first
        else:
            return best
            
    return densest_helper(rc_list).region.name
    

#Task 4
def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    #Returns a new RegionCondition representing the projected state of the region after the given number of years.
    def terrain_helper(rc: RegionCondition) -> float:
        if rc.region.terrain == "ocean":
            return 0.0001
        elif rc.region.terrain == "mountains":
            return 0.0005
        elif rc.region.terrain == "forest":
            return -0.00001
        elif rc.region.terrain == "other":
            return 0.0003
    
    def projected_pop(population: int, rate: float, years: int) -> float:
        if years == 0:
            return population
        return projected_pop(population * (1 + rate), rate, years - 1)

    
    growth_rate = terrain_helper(rc)
    new_pop = int(projected_pop(rc.pop, growth_rate, years))

    if rc.pop == 0:
        new_ghg = 0.0
    else:
        new_ghg = rc.ghg_rate * (new_pop / rc.pop)
        
    new_year = rc.year + years
    region = rc.region
    
    return RegionCondition(region, new_year, new_pop, new_ghg)#complete your tasks in this file
