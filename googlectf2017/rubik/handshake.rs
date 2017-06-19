use permutation::Permutation;
use cube::Cube;
use crypto::blake2b::Blake2b;

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
pub struct SecretKey {
    pub a: u64,
    pub b: u64,
}

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
pub struct PublicKey {
    pub key: Permutation,
}

impl SecretKey {
    pub fn to_public(&self) -> PublicKey {
        let pa = Permutation::parse("U x'").unwrap();
        let pb = Permutation::parse("L y'").unwrap();

        PublicKey { key: self.a * pa + self.b * pb }
    }

    pub fn handshake(&self, key: PublicKey, salt: &[u8]) -> [u8; 16] {
        let pa = Permutation::parse("U x'").unwrap();
        let pb = Permutation::parse("L y'").unwrap();
        let cube = Cube::default().apply(self.a * pa + key.key + self.b * pb);
        let mut out = [0; 16];
        Blake2b::blake2b(&mut out, &cube.serialize().as_bytes(), salt);
        out
    }
}

impl PublicKey {
    pub fn serialize(&self) -> String {
        Cube::default().apply(self.key).serialize()
    }

    pub fn unserialize(s: &str) -> Option<PublicKey> {
        if let Some(cube) = Cube::unserialize(s) {
            if let Some(perm) = Permutation::from_cube(cube) {
                return Some(PublicKey { key: perm });
            }
        }
        None
    }
}
