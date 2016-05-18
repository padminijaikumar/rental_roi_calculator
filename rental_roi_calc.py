__author__ = 'padminijaikumar'

import math
import numpy
#Calculate Rental ROI

##Inputs
house_cost=233000 #total cost: land + house
depreciable_value=0.7 #% of house_cost that is the house
monthly_rent=1700
analysis_for_n_years=10
rent_increase_rate=0.06
house_appreciation_rate=0.06
mortgage_rate=0.02625
mortgage_duration=15
down_payment=0.20


##Other rates that impact calculation. Need not be changed.
property_tax_rate=0.0235
insurance_rate=0.01
prop_management_rate = 0.08 #% of rent
one_time_lease_cost_per_year=1000
yearly_maintenance=2000
months_vacant=1
closing_fees=2000
selling_costs=0.04 #% of house cost
yearly_trip=250
one_time_fixup_before_selling=20000
hoa_per_month=30



### Grand Totals
net_earnings_over_analysis_years_from_rent_after_tax=0
total_money_spent_on_house=0
total_depreciation_claimed=0

loan_principal_balance=(1-down_payment)*house_cost
net_cash_flow_arr = []
for year in range(1, analysis_for_n_years+1):
    ####################### Calculate Cash In ##########################################################
    cash_in=0

    ### Rent for 12 months (Vacancy accounted for in Cash Out) ######
    if year == 1:
        yearly_rent=monthly_rent*12
    else:
        yearly_rent=(1+rent_increase_rate)*yearly_rent
    cash_in+=yearly_rent


    ####################### Calculate Cash Out and Tax Deductible ######################################
    cash_out=0

    tax_deductible_expenses=0

    ###### Mortgage Payments ####
    #For formula see: http://www.mtgprofessor.com/formulas.htm
    yearly_mortgage_payment=0
    if loan_principal_balance > 0:
        for month in range(1,12):
            #Calculate monthly payment, new principal, principal component and interest component
            monthly_mortgage_payment=loan_principal_balance * (mortgage_rate/12)*math.pow(1+mortgage_rate/12, mortgage_duration*12) / (math.pow(1+mortgage_rate/12, mortgage_duration*12) - 1)
            new_loan_principal_balance = loan_principal_balance*(math.pow(1+mortgage_rate/12, mortgage_duration*12) - (1+mortgage_rate/12))/(math.pow(1+mortgage_rate/12, mortgage_duration*12) - 1)
            yearly_mortgage_payment+=monthly_mortgage_payment
            principal_component=loan_principal_balance-new_loan_principal_balance
            interest_component=monthly_mortgage_payment-principal_component

            #Set new loan_principal_balance
            loan_principal_balance=new_loan_principal_balance

            #add mortgage payment to cash_out and interest_component to tax_deductible_expense
            cash_out+=principal_component+interest_component
            #cash_out+=interest_component

            tax_deductible_expenses+=interest_component


    ###### Property Tax #########
    if year == 1:
        appreciated_house_value=house_cost
    else:
        appreciated_house_value = (1+house_appreciation_rate)*appreciated_house_value
    property_tax = property_tax_rate*appreciated_house_value

    #Add to cash out and tax deductible
    cash_out+=property_tax
    tax_deductible_expenses+=property_tax


    ##### Property Management, HOA, Vacancy, Maintenance ####
    yearly_prop_management=yearly_rent*prop_management_rate
    yearly_hoa=hoa_per_month*12
    yearly_vacancy=yearly_rent*months_vacant/12


    yearly_fixed_expenses=yearly_prop_management+yearly_hoa+yearly_vacancy+yearly_maintenance+yearly_trip
    cash_out+=yearly_fixed_expenses
    tax_deductible_expenses+=yearly_fixed_expenses


    ##### House Depreciation #########
    yearly_depreciation=depreciable_value*house_cost/27.5
    tax_deductible_expenses+=yearly_depreciation
    #Depreciation claimed so far
    total_depreciation_claimed+=yearly_depreciation


    ####################### Print Results, and Update totals Results for the year ########################################

    ### Determine cash flow and tax impact per year
    net_cash_flow=cash_in-cash_out
    if year==1:
        net_cash_flow-=down_payment*house_cost + closing_fees
    net_cash_flow_arr.append(net_cash_flow)
    tax_impact=cash_in-tax_deductible_expenses
    print "Year " + str(year) + "-> Net Cash Flow:" + str(net_cash_flow) + ", Tax Impact: " + str(tax_impact)

    ### Add to net earning over analysis years
    #If tax impact > 0, we made money. Add to net_earnings after deducting 33% tax
    if tax_impact > 0:
        net_earnings_over_analysis_years_from_rent_after_tax+=0.66*tax_impact

    #If net_cash_flow <0, we lost money. For taxes we made $0, cannot deduct losses. So add this to money spent on house
    if net_cash_flow < 0:
        total_money_spent_on_house+=abs(net_cash_flow)


###### At the end of n years calculate net earning and ROI ######
print "Selling House Numbers"
print "Appreciated House Value after " + str(analysis_for_n_years) + " years: " + str(appreciated_house_value)
earning_from_selling_house = (1-selling_costs)*appreciated_house_value - loan_principal_balance
gain_from_selling_house_after_tax = 0.85*earning_from_selling_house - 0.25*total_depreciation_claimed
total_earnings_after_n_years= gain_from_selling_house_after_tax + net_earnings_over_analysis_years_from_rent_after_tax
roi = (total_earnings_after_n_years - total_money_spent_on_house)*100/(total_money_spent_on_house*analysis_for_n_years)


########## IRR #################################
net_cash_flow_arr.append(gain_from_selling_house_after_tax)
final_irr = numpy.irr(net_cash_flow_arr)*100
print "After Tax IRR: " + str(final_irr)


print "Earnings after " + str(analysis_for_n_years) + " years -> " + "Total: " + str(total_earnings_after_n_years) + \
    ", From yearly rent - expenses: " + str(net_earnings_over_analysis_years_from_rent_after_tax) + ", Selling house: " + str(gain_from_selling_house_after_tax)
print "Total Money spent on house: " + str(total_money_spent_on_house)
print "Simple ROI per year (after tax): " + str(roi)





