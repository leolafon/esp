import pandas as pd
import numpy as np

def main(*args, **kwargs):
  chunksize = 1000
  df = pd.read_excel("toto.xlsx")
  for chunk in np.array_split(df, len(df) // chunksize):
      chunk.to_excel('result_{:02d}.xlsx'.format(1), index=False)
      break

if __name__ == "__main__":
  main()
