# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# See http://wiki.archlinux.org/index.php/Python_Package_Guidelines for more
# information on Python packaging.

# Maintainer: Ben Spiers <ben.spiers22@gmail.com>
pkgname=python-xbmcremote
pkgver=1
pkgrel=1
pkgdesc="Program for controlling XBMC running on other computers"
arch=(any)
url=""
license=('GPL')
groups=()
depends=('python2' 'python2-gobject' 'python2-dbus' 'python-quickly.widgets')
makedepends=('python-distutils-extra')
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=()
md5sums=()

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python2.7 setup.py install --root="$pkgdir/" --optimize=1
}

# vim:set ts=2 sw=2 et:
