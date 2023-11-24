# Maven Uploader

```
-r 本地仓库路径

-t 远程仓库url

-d 参数可选，填相对于 -r (本地仓库根目录) 的相对路径。 如果填了，就表示只传这个相对路径下的包。 如果不填，就是传本地仓库目录下的所有包

-v 参数，  打印 mvn deploy 命令的详情

eg.

python3 maven-repo-tools.py -r '/tmp/repo' -t 'https://maven.xxx.xxx/repository/maven-snapshots' -d 'com/xxx/xxx'

```
