import argparse
from os import walk
import subprocess

parser = argparse.ArgumentParser(prog='Maven Repo Tools')
parser.add_argument('-r', '--rootpath', required=True)  
parser.add_argument('-t', '--target', required=True)  
parser.add_argument('-d', '--directory')  
parser.add_argument('-u', '--username')  
parser.add_argument('-p', '--password')  
parser.add_argument('-v', '--verbose', action='store_true')  

args = parser.parse_args()

target = args.target
if target.endswith('/'):
    target = target[0:-1]
repoId = target.split('/')[-1:][0]
print('target:',target, 'repoId:', repoId)

path = args.rootpath
if args.directory:
    path += '/' + args.directory

print('walking path:', path)
w = walk(path)
for (dirpath, dirnames, filenames) in w:
    isleaf = False
    onlyPom = True 
    for filename in filenames:
        if filename.endswith('.pom'):
            isleaf = True
        if filename.endswith('.jar'):
            onlyPom = False
    if isleaf:
        package_path_arr = dirpath[len(args.rootpath):].replace('//', '/').split('/')
        groupId = '.'.join(package_path_arr[0:-2])
        if groupId.startswith('.'):
            groupId = groupId[1:]
        artifactId = package_path_arr[-2:-1][0]
        version = package_path_arr[-1:][0]
        if onlyPom:
            for filename in filenames:
                if filename.endswith('.pom'):
                    cmd = ['mvn', 'deploy:deploy-file', '-Durl='+target, '-DgroupId='+groupId, '-DartifactId='+artifactId, '-Dversion='+version, '-DrepositoryId='+repoId, '-Dpackaging=pom', '-Dfile='+dirpath+'/'+filename]
                    break
        else:
            cmd = ['mvn', 'deploy:deploy-file', '-Durl='+target, '-DgroupId='+groupId, '-DartifactId='+artifactId, '-Dversion='+version, '-DrepositoryId='+repoId, '-DgeneratePom=false']
            has_pom=False
            has_file=False
            has_sources=False
            for filename in filenames:
                if not has_pom and filename.endswith('.pom'):
                    cmd.append('-DpomFile='+dirpath+'/'+filename)
                    has_pom = True
                if not has_file and filename.endswith('.jar') and not filename.endswith('-sources.jar'):
                    cmd.append('-Dfile='+dirpath+'/'+filename)
                    has_file = True
                if not has_sources and filename.endswith('-sources.jar'):
                    cmd.append('-Dsources='+dirpath+'/'+filename)
                    has_sources = True

        print('deploying', groupId+':'+artifactId+':'+version)
        if args.verbose:
            print(' '.join(cmd))
        result = subprocess.run(cmd, capture_output=True)
        if args.verbose:
            print(repr(result.stdout))


