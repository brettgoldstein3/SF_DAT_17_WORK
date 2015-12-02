# pulls data from internal Google tables
# only includes timeseries data for Free iOS apps in the US
select f.app_id,
       f.week_id,
       f.month_id,
       f.primary_category,
       f.rating_count_cur,
       f.rating_avg_all,
       f.downloads,
       f.appannie_url,
       d.rank,
       d.rank_category,
       d.days_ranked,
       d.primary_category
from (select app_id, app_name, month_id, week_id, primary_category,
         rating_count_cur, rating_count_all, rating_avg_all, downloads, appannie_url
      from MADW_AppEstimates_F
      where download_country_code == "US"
	   and store == "iOS"
       and app_type == "Free"
       and device == "iPhone"
      GROUP@100 BY 1,2,3,4,5,6,7,8,9,10) f
join@1000
     (select app_id, app_name, month_id, week_id,
        rank, rank_category, days_ranked, primary_category
      from MADW_AppRankings_D
      where download_country_code == "US"
	    and store == "iOS"
        and rank_category == 'Overall'
        and rank_type == "Free"
        and device == "iPhone"      
      GROUP@100 BY 1,2,3,4,5,6,7,8) d
on d.app_id = f.app_id and d.week_id = f.week_id