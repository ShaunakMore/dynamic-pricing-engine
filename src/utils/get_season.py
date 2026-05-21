def getSeason(month:int) -> str:
  """
  Function to return the season (according to seasons in the Indian subcontinent) 
  based on month of the year
  """
  if 3 <= month <= 6:
    return "Summer"
  
  elif 7 <= month <= 9:
    return "Monsoon"
  
  else:
    return "Winter"