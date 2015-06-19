package cn.edu.tsinghua.thss.popcorn;

import java.util.ArrayList;
import java.util.List;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.util.DisplayMetrics;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.beardedhen.androidbootstrap.FontAwesomeText;

import cn.edu.tsinghua.thss.popcorn.QRcode.QRcodeActivity;
import cn.edu.tsinghua.thss.popcorn.ui.AppsFragment;
import cn.edu.tsinghua.thss.popcorn.ui.FragmentAdapter;
import cn.edu.tsinghua.thss.popcorn.ui.MineFragment;
import cn.edu.tsinghua.thss.popcorn.ui.RecordFragment;
import cn.edu.tsinghua.thss.popcorn.ui.ReportFragment;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class MainActivity extends FragmentActivity {

	private ViewPager mPageVp;

	private List<Fragment> mFragmentList = new ArrayList<Fragment>();
	private FragmentAdapter mFragmentAdapter;

	private TextView mTabRecordTv, mTabRepairTv, mTabAppsTv, mTabMineTv;

    private FontAwesomeText mTabRecordFat, mTabRepairFat, mTabAppsFat, mTabMineFat;

    private View mTabRecordLayout, mTabRepairLayout, mTabAppsLayout, mTabMineLayout;
	/**
	 * Tab的那个引导线
	 */
	private ImageView mTabLineIv;
	/**
	 * Fragment
	 */
	private RecordFragment mRecordFg;
	private ReportFragment mRepairFg;
    private AppsFragment mAppsFg;
    private MineFragment mMineFg;
	/**
	 * ViewPager的当前选中页
	 */
	private int currentIndex;

	/**
	 * 屏幕的宽度
	 */
	private int screenWidth;

    /**
     * tab 的数量
     */
    private int numOfTabs = 4;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
		findById();
		init();
		initTabLineWidth();
	}

	private void findById() {
		mTabRecordTv = (TextView) this.findViewById(R.id.id_record_tv);
        mTabRepairTv = (TextView) this.findViewById(R.id.id_repair_tv);
        mTabAppsTv = (TextView) this.findViewById(R.id.id_apps_tv);
        mTabMineTv = (TextView) this.findViewById(R.id.id_mine_tv);

        mTabRecordFat = (FontAwesomeText) findViewById(R.id.id_record_fat);
        mTabRepairFat = (FontAwesomeText) findViewById(R.id.id_repair_fat);
        mTabAppsFat = (FontAwesomeText) findViewById(R.id.id_apps_fat);
        mTabMineFat = (FontAwesomeText) findViewById(R.id.id_mine_fat);

        mTabRecordLayout = this.findViewById(R.id.id_tab_record_ll);
        mTabRepairLayout = this.findViewById(R.id.id_tab_repair_ll);
        mTabAppsLayout = this.findViewById(R.id.id_tab_apps_ll);
        mTabMineLayout = this.findViewById(R.id.id_tab_mine_ll);

		mTabLineIv = (ImageView) this.findViewById(R.id.id_tab_line_iv);
		mPageVp = (ViewPager) this.findViewById(R.id.id_page_vp);
	}

	private void init() {
		mRecordFg = new RecordFragment();
		mRepairFg = new ReportFragment();
        mAppsFg = new AppsFragment();
        mMineFg = new MineFragment();

        mFragmentList.add(mAppsFg);
		mFragmentList.add(mRecordFg);
		mFragmentList.add(mRepairFg);
        mFragmentList.add(mMineFg);

		mFragmentAdapter = new FragmentAdapter(this.getSupportFragmentManager(), mFragmentList);
		mPageVp.setAdapter(mFragmentAdapter);
		mPageVp.setCurrentItem(0);

        mTabAppsLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(0, false);
            }
        });

        mTabRecordLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(1, false);
            }
        });

        mTabRepairLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(2, false);
            }
        });

        mTabMineLayout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mPageVp.setCurrentItem(3, false);
            }
        });

		mPageVp.setOnPageChangeListener(new OnPageChangeListener() {

			/**
			 * state滑动中的状态 有三种状态（0，1，2） 1：正在滑动 2：滑动完毕 0：什么都没做。
			 */
			@Override
			public void onPageScrollStateChanged(int state) {
                // code goes here
			}

			/**
			 * position :当前页面，及你点击滑动的页面 offset:当前页面偏移的百分比
			 * offsetPixels:当前页面偏移的像素位置
             * This method will be invoked when the current page is scrolled
			 */
			@Override
			public void onPageScrolled(int position, float offset,
					int offsetPixels) {
				LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
						.getLayoutParams();

				//Log.e("offset:", offset + "");
				/**
				 * 利用currentIndex(当前所在页面)和position(下一个页面)以及offset来
				 * 设置mTabLineIv的左边距 滑动场景：
				 * 记4个页面,
				 * 从左到右分别为0,1,2, 3
				 */

				if (currentIndex == 0 && position == 0)// 0->1
				{
					lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));

				} else if (currentIndex == 1 && position == 0) // 1->0
				{
					lp.leftMargin = (int) (-(1 - offset)
							* (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));

				} else if (currentIndex == 1 && position == 1) // 1->2
				{
					lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));
				} else if (currentIndex == 2 && position == 1) // 2->1
				{
					lp.leftMargin = (int) (-(1 - offset)
							* (screenWidth * 1.0 / numOfTabs) + currentIndex
							* (screenWidth / numOfTabs));
				} else if (currentIndex == 2 && position == 2) // 2->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                } else if (currentIndex == 3 && position == 2) // 3->2
                {
                    lp.leftMargin = (int) (-(1 - offset)
                            * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                }else if (currentIndex == 3 && position == 3) // 3->3
                {
                    lp.leftMargin = (int) (offset * (screenWidth * 1.0 / numOfTabs) + currentIndex
                            * (screenWidth / numOfTabs));
                }
                mTabLineIv.setLayoutParams(lp);
			}


            // This method will be invoked when a new page becomes selected.
			@Override
			public void onPageSelected(int position) {
				resetTabColor();
				switch (position) {
                    case 0:
                        mTabAppsTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabAppsFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 1:

                        mTabRecordTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRecordFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 2:
                        mTabRepairTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabRepairFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
                    case 3:
                        mTabMineTv.setTextColor(Color.parseColor("#33B5E5"));
                        mTabMineFat.setTextColor(Color.parseColor("#33B5E5"));
                        break;
				}
				currentIndex = position;
			}
		});

	}

	/**
	 * 设置滑动条的宽度为屏幕的1/4(根据Tab的个数而定)
	 */
	private void initTabLineWidth() {
		DisplayMetrics dpMetrics = new DisplayMetrics();
		getWindow().getWindowManager().getDefaultDisplay()
				.getMetrics(dpMetrics);
		screenWidth = dpMetrics.widthPixels;
		LinearLayout.LayoutParams lp = (LinearLayout.LayoutParams) mTabLineIv
				.getLayoutParams();
		lp.width = screenWidth / numOfTabs;
		mTabLineIv.setLayoutParams(lp);
	}

	/**
	 * 重置导航栏的颜色
	 */
	private void resetTabColor() {
		mTabRecordTv.setTextColor(Color.parseColor("#D3D3D3"));
		mTabRepairTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsTv.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineTv.setTextColor(Color.parseColor("#D3D3D3"));

        mTabRecordFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabRepairFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabAppsFat.setTextColor(Color.parseColor("#D3D3D3"));
        mTabMineFat.setTextColor(Color.parseColor("#D3D3D3"));
	}


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        switch (item.getItemId()){
            case R.id.scan_btn:
                Intent intent=new Intent(this, QRcodeActivity.class);
                Bundle bundle=new Bundle();
                intent.putExtras(bundle);
                startActivity(intent);
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }
}
