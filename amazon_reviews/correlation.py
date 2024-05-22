import os
import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr
import seaborn as sns
con = duckdb.connect("amazon_reviews.duckdb")

# Looks at the dataset as a whole

queryProductsWithVine = "SELECT Distinct product_id, product_title FROM amazon_reviews_multilingual_US_v1_00 WHERE vine='Y' ORDER BY product_id"
productDf = con.sql(queryProductsWithVine).df()
productWithVineList = productDf['product_id'].tolist()
# Construct SQL query to get all reviews for these products containing vine reviews and not containing vine reviews on the whole dataset 
product_ids = "', '".join(productWithVineList)  # Join product IDs as a comma-separated string
query = "SELECT distinct review_id, product_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids)
query2 = "SELECT distinct review_id, product_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids) + " AND vine ='Y'"
query3 = "SELECT distinct review_id, product_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids) + " AND vine ='N'"

# Execute SQL query to get reviews for these products
df = con.sql(query).df()
df['vine'] = df['vine'].replace({'Y': True, 'N': False})

df2 = con.sql(query2).df()
df3 = con.sql(query3).df()

# X = df[['vine', 'helpful_votes']].copy()
# helpfulvineCorr, pVal = pointbiserialr(X['vine'], X['helpful_votes'])
# print("Correlation Between Vine and Helpful Votes: ", helpfulvineCorr)
# print("P-value: ", pVal)


print("Pearson: ", df["vine"].corr(df['star_rating'], method="pearson"))
print("Kendall: ", df["vine"].corr(df['star_rating'], method='kendall'))
print("Spearmen: ", df["vine"].corr(df['star_rating'], method='spearman'))
correlation_vine_rating1, p_value1 = pointbiserialr(df['vine'], df['star_rating'])
print("correlation_vine_rating: ", correlation_vine_rating1)
print("p_value: ", p_value1)
        

#print(vinereviews_df)
        
avgVineRatingWhole = df2['star_rating'].mean(skipna=True)
avgNonVineRatingWhole = df3['star_rating'].mean(skipna=True)     
        
print("Average Star Rating for Vine Reviews on the whole dataset: ", avgVineRatingWhole)
print("Average Star Rating for Non-Vine Reviews on the whole dataset: ", avgNonVineRatingWhole)

dataToCSV = pd.DataFrame({
    "Avg SR For Vine Reviews" : [avgVineRatingWhole],
    "Avg SR For Non-Vine Reviews" : [avgNonVineRatingWhole],
    "Pearson Corr" : [df["vine"].corr(df['star_rating'], method="pearson")],
    "Kendall Corr" : [df["vine"].corr(df['star_rating'], method='kendall')],
    "Spearmen Corr" : [df["vine"].corr(df['star_rating'], method='spearman')],
    "Biserial Corr" : [correlation_vine_rating1],
    "P-value" : [p_value1]
})

dataToCSV.to_csv(os.path.join(os.getcwd() + "/data/", "data.csv"), index=False)














# This gets the average star_rating for amazon vine reviews on the whole dataset
queryAvgVineRating = "SELECT AVG(star_rating) FROM amazon_reviews_multilingual_US_v1_00 WHERE vine='Y'"
avgVineRating = con.sql(queryAvgVineRating).show()


# This gets the average star_rating for amazon non-vine reviews for the whole dataset
queryAvgNonVineRating = "SELECT AVG(star_rating) FROM amazon_reviews_multilingual_US_v1_00 WHERE vine='N'"
avgNoneVineRating = con.sql(queryAvgNonVineRating).show()











# Looks at the dataset from a individual product category prespective
# print("=========================================")
# Gets the product categories from the amazon review dataset
sqlCategories = "SELECT DISTINCT product_category FROM amazon_reviews_multilingual_US_v1_00 ORDER BY product_category"
dfCategories = con.sql(sqlCategories)
numpyCategories = dfCategories.fetchnumpy()
print(numpyCategories)

rating_dict = {}
category_set = list()
vine_set = list()
nonvine_set = list()
corr_dict = {}
corr_value = list()
p_value_list = list()
vineRatingDict = {}
vineList = []
ratingList = []
catList = []
prodList = []


# Takes in a string (category), queries the SQL database for the category, and performs correlation between the ratings of vine reviews and non-vine reviews for each category
def categorySQLToPlot(category, j):
    sqlVotes0 = "SELECT COUNT(vine) FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + category + "AND vine='Y'"
    dfVotes0 = con.sql(sqlVotes0)
    #print(dfVotes0)
    numpyVotes = dfVotes0.df()
    #print(numpyVotes['count(vine)'][0])
    
    if numpyVotes['count(vine)'][0] != 0:
        print("------------------------------------------------------------------")
        print(category)
        
        # Gets All the products in a category that has a vine review, so we don't have to worry about products that don't contain any vine reviews
        sqlDistinctProducts = "SELECT Distinct product_id, product_title FROM amazon_reviews_multilingual_US_v1_00 WHERE product_category = " + category + " AND vine='Y' ORDER BY product_id"
        distinctProductDf = con.sql(sqlDistinctProducts).df()
        
        # Converts the all the distinct products to a list
        product_ids = distinctProductDf['product_id'].tolist()
        
        # Construct SQL query to get all reviews for these products that received a review by a vine member
        product_ids_str = "', '".join(product_ids)  # Join product IDs as a comma-separated string
        query_reviews = "SELECT distinct review_id, product_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids_str)
    
        # Execute query and convert result into a dataframe
        reviews_df = con.sql(query_reviews).df()
        
        # Replace values to True and False
        reviews_df['vine'] = reviews_df['vine'].replace({'Y': True, 'N': False})
        
        # Compute Point-Biserial correlation
        biserialCorr, pValue = pointbiserialr(reviews_df['vine'], reviews_df['star_rating'])
        print("correlation_vine_rating: ", biserialCorr)
        print("p_value: ", pValue)
        
        print("Pearson: ", reviews_df["vine"].corr(reviews_df['star_rating'], method="pearson"))
        print("Kendall: ", reviews_df["vine"].corr(reviews_df['star_rating'], method='kendall'))
        print("Spearmen: ", reviews_df["vine"].corr(reviews_df['star_rating'], method='spearman'))
        
         
        query_vinereviews = "SELECT distinct review_id, product_id, star_rating, vine FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids_str) + " AND vine ='Y'"
        query_nonvinereviews = "SELECT distinct review_id, product_id, star_rating, vine FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id IN ('{}')".format(product_ids_str) + " AND vine ='N'"
        vinereviews_df = con.sql(query_vinereviews).df()
        nonvinereviews_df = con.sql(query_nonvinereviews).df()
        #print(vinereviews_df)
        
        avgVineReviewRating = vinereviews_df['star_rating'].mean(skipna=True)
        avgNonVineReviewRating = nonvinereviews_df['star_rating'].mean(skipna=True)     
        
        print("Average Star Rating for Vine Reviews: ", avgVineReviewRating)
        print("Average Star Rating for Non-Vine Reviews: ", avgNonVineReviewRating)
        
        category_set.append(category)
        vine_set.append(round(avgVineReviewRating, 2))
        nonvine_set.append(round(avgNonVineReviewRating, 2))
        corr_value.append(biserialCorr)
        p_value_list.append(pValue)
        rating_dict['AVG SR Vine'] = vine_set
        rating_dict['AVG SR Non-Vine'] = nonvine_set
        corr_dict["Product Category"] = category_set
        corr_dict["Correlation"] = corr_value
        corr_dict['P-Value'] = p_value_list
        
        # plt.scatter(reviews_df['vine'], reviews_df['star_rating'])
        # plt.plot(np.unique(reviews_df['vine']), np.poly1d(np.polyfit(reviews_df['vine'], reviews_df["star_rating"], 1))
        # (np.unique(reviews_df["vine"])), color='red')
        # plt.show()
        
        
        # Writes Data to csv file
        data = pd.DataFrame({
            "AVG Vine Star_Rating": [avgVineReviewRating],
            "AVG Non-Vine Star Rating: ": [avgNonVineReviewRating],
            "Pearson Corr" : [reviews_df["vine"].corr(reviews_df['star_rating'], method="pearson")],
            "Kendall Corr" : [reviews_df["vine"].corr(reviews_df['star_rating'], method='kendall')],
            "Spearmen Corr" : [ reviews_df["vine"].corr(reviews_df['star_rating'], method='spearman')],
            "Biserial Corr" : [biserialCorr],
            "P-value" : [pValue]
        })
        # data = pd.DataFrame(list(zip(avgVineReviewRating, avgNonVineReviewRating)), columns=["Avg Vine SR", "Avg NonVine SR"])
        data.to_csv(os.path.join(os.getcwd() + "/data/", "{}.csv".format(category)), index=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        first = 1

        # Goes through each product that has a vine review
        for i in range(len(distinctProductDf['product_id'])):
                # This gets all the vine reviews on a product and gets its mean star_rating
                # print('vine reviews on ' + numpyVotes3['product_id'][i] + ' ' + numpyVotes3['product_title'][i])
                sqlQuery = "SELECT DISTINCT review_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id = " + "'" + distinctProductDf['product_id'][i] + "'" + " AND vine='Y'"
                result = con.sql(sqlQuery)
                resultdf = result.df()
                #print(resultdf)
                print(resultdf['star_rating'].mean())
                
                # This Gets All the non-vine reviews on a product and gets its mean star_rating
                # print("non-vine reviews on products")
                sqlQuery2 = "SELECT DISTINCT review_id, star_rating, vine, verified_purchase, helpful_votes FROM amazon_reviews_multilingual_US_v1_00 WHERE product_id = " + "'" + distinctProductDf['product_id'][i] + "'" + " AND vine='N'"
                result2 = con.sql(sqlQuery2)
                resultdf2 = result2.df()
                #print(resultdf2)
                print(resultdf2['star_rating'].mean())
                print('\n')
                
                mean = resultdf['helpful_votes'].mean()
                mean2 = resultdf2['helpful_votes'].mean()

                if np.isnan(mean) == False and np.isnan(mean2) == False:
                    prodList.append(distinctProductDf['product_id'][i])
                    catList.append(category)
                    prodList.append(distinctProductDf['product_id'][i])
                    catList.append(category)
                    vineList.append(True)
                    vineList.append(False)
                    ratingList.append(resultdf['helpful_votes'].mean())
                    ratingList.append(resultdf2['helpful_votes'].mean())
                    vineRatingDict['product_id'] = prodList
                    vineRatingDict['product_category'] = catList
                    vineRatingDict['vine'] = vineList
                    vineRatingDict['avg_helpful_votes'] = ratingList
                
                if first == 1:
                    data2 = pd.DataFrame({
                            "Product ID": [distinctProductDf['product_id'][i]],
                            "Avg Vine SR": [resultdf['star_rating'].mean()],
                            "Avg NonVine SR": [resultdf2['star_rating'].mean()]
                        })
                    #data2 = pd.DataFrame(list(zip(numpyVotes3['product_id'], [resultdf['star_rating'].mean()], [resultdf2['star_rating'].mean()])), columns=["Product ID", "Avg Vine SR", "Avg NonVine SR"])
                    data2.to_csv(os.path.join(os.getcwd() + "/data/", "{}.csv".format(category)), mode='a', index=False)
                    first = first - 1
                else:
                    data2 = pd.DataFrame({
                            "Product ID": [distinctProductDf['product_id'][i]],
                            "Avg Vine SR": [resultdf['star_rating'].mean()],
                            "Avg NonVine SR": [resultdf2['star_rating'].mean()]
                        })
                    #data2 = pd.DataFrame(list(zip(numpyVotes3['product_id'], [resultdf['star_rating'].mean()], [resultdf2['star_rating'].mean()])), columns=["Product ID", "Avg Vine SR", "Avg NonVine SR"])
                    data2.to_csv(os.path.join(os.getcwd() + "/data/", "{}.csv".format(category)), mode='a', header=False, index=False)
            
        print("------------------------------------------------------------------")
        
         
        
        
            
        
        
    
# print("Printing the categories in the plot")
# Now we need to get the total votes and helpful votes for each category
#We'll make a for loop that goes through each category and calls the function
for i in range(len(numpyCategories['product_category'])):
    categorySQLToPlot("'" + numpyCategories['product_category'][i] + "'", i)
print("Done printing the categories in the plot")

print(corr_dict)

correlation_df = pd.DataFrame(corr_dict)
print(correlation_df)
correlation_df.to_csv(os.path.join(os.getcwd() + "/data/", "correlation.csv"), index=False)

corr_df = pd.DataFrame(vineRatingDict)
helpfulvineCorr, pVal = pointbiserialr(corr_df['vine'], corr_df['avg_helpful_votes'])
print(corr_df)
print("Correlation Between Vine and Helpful Votes: ", helpfulvineCorr)
print("P-value: ", pVal)

# Plot the correlation using Seaborn
# Plot the scatter plot
# plt.scatter(corr_df['vine'], corr_df['avg_helpful_votes'], label='Data points')

# # Fit a best-fit line (linear regression)
# coefficients = np.polyfit(corr_df['vine'], corr_df['avg_helpful_votes'], 1)
# line = np.poly1d(coefficients)
# plt.plot(corr_df['vine'], line(corr_df['vine']), color='red', label='Best-fit line')
# plt.xticks([0, 1], ['False', 'True'])

# plt.title('Correlation Between Vine and Helpful Votes')
# plt.xlabel('Vine')
# plt.ylabel('Avg Helpful Votes')
# plt.legend()
# plt.show()

plt.scatter(df['vine'], df['star_rating'], label='Data points')
# # Fit a best-fit line (linear regression)
coefficients = np.polyfit(df['vine'], df['star_rating'], 1)
line = np.poly1d(coefficients)
plt.plot(df['vine'], line(df['vine']), color='red', label='Best-fit line')
plt.xticks([0, 1], ['False', 'True'])

plt.title('Correlation Between Vine and Star Ratings')
plt.xlabel('Vine')
plt.ylabel('Star Ratings')
plt.legend()
plt.show()


x = np.arange(len(category_set))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in rating_dict.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute, align="center")
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Star Ratings')
ax.set_title('Product Categories')
ax.set_xticks(x + width, category_set, rotation = 45)
ax.legend(loc='upper left', ncols=2)
ax.set_ylim(0, 5)

plt.show()


