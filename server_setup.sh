# setup vimrc
echo "setting up vimrc"
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
wget https://raw.githubusercontent.com/syllogismos/dotfiles/master/vim/vimrc.symlink
mv vimrc.symlink ~/.vimrc

# setup gitconfig
echo "setting up gitconfig"
wget https://raw.githubusercontent.com/syllogismos/dotfiles/master/git/gitconfig.server
mv gitconfig.server ~/.gitconfig