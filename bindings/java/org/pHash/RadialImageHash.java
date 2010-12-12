package org.pHash;

/**
 *
 * @author Christoph Zauner
 */
public class RadialImageHash extends ImageHash {
	
	private byte[] hash;

	/**
	 * @return the hash
	 */
	public byte[] getHash() {
		return hash;
	}

	/**
	 * @param hash the hash to set
	 */
	public void setHash(byte[] hash) {
		this.hash = hash;
	}
}
