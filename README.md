### git 指令

```
git config --global user.name 'name' //配置用户名
git config --global user.email 'email@address' //配置邮箱
ssh-keygen -t rsa -C 'emial@address' //生成ssh密钥文件
git status //查看状态
git add . //将工作区变更压入暂存区
git commit -m 'comment' //将暂存区内容提交至仓库
git log --pretty=oneline //单行显示日志
git reset --hard 'commit id' //回退到某个版本
git reflog //为了从过去版本切回最新版本，需要使用此命令查看历史的commit id
git clone 网址 //从线上克隆项目到本地
git push //将本地的变更提交至线上
git pull //将线上的变更拉取到本地
git branch //查看分支
git branch 分支名 //创建分支
git branch -d 分支名 //删除分支
git checkout 分支名 //切换分支
git checkout -b 分支名 //创建一个新的分支并切换过去
git merge 被合并的分支名 //合并分支
```

