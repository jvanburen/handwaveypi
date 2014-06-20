import test, cProfile, pstats

cProfile.run('test.main()', 'profile_results')

p = pstats.Stats('profile_results')


