package org.pHash;

import java.math.BigInteger;

/**
 *
 * @author Christoph Zauner
 */
public class BMBImageHash extends ImageHash {

	private byte[] hash;

	@Override
	public String toString() {
		BigInteger bigInteger = new BigInteger(hash);
		return bigInteger.toString(2);
	}

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

} // end of class
