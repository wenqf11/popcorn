package cn.edu.tsinghua.thss.popcorn.ui;

import java.util.ArrayList;
import java.util.List;

import android.support.v4.app.FragmentTransaction;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;

import cn.edu.tsinghua.thss.popcorn.R;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class FragmentAdapter extends FragmentPagerAdapter {
	private List<Fragment> mFragments;

	public FragmentAdapter(FragmentManager fm) {
		super(fm);
	}

	public FragmentAdapter(FragmentManager fm,List<Fragment> fragments) {
		super(fm);
		this.mFragments = fragments;
	}

	@Override
	public Fragment getItem(int position) {
		return mFragments.get(position);
	}

	@Override
	public int getCount() {
		return mFragments.size();
	}

	@Override
	public int getItemPosition(Object object) {
		return POSITION_NONE;
	}

	public void setFragmentsList(FragmentManager fm, List<Fragment> fragments){
		if (this.mFragments != null) {
			FragmentTransaction ft = fm.beginTransaction();
			for (Fragment f : this.mFragments) {
				ft.remove(f);
			}
			ft.commit();
			ft = null;
			fm.executePendingTransactions();
		}
		this.mFragments = fragments;
		notifyDataSetChanged();
	}
}
